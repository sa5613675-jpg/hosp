"""
PC (Persistent Commission) System Views
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import PCMember, PCTransaction
from patients.models import Patient
from appointments.models import Appointment

@login_required
def pc_member_list(request, member_type):
    """List PC members by type (Admin only)"""
    if not request.user.is_admin:
        messages.error(request, "Access denied. Admin only.")
        return redirect('accounts:dashboard')
    
    # Validate member type
    valid_types = {'GENERAL', 'LIFETIME', 'PREMIUM'}
    if member_type not in valid_types:
        messages.error(request, "Invalid member type.")
        return redirect('accounts:pc_dashboard')
    
    # Get search parameter
    search = request.GET.get('search', '')
    
    # Base query - filter by member type
    members = PCMember.objects.filter(member_type=member_type)
    
    # Apply search filter
    if search:
        members = members.filter(
            Q(pc_code__icontains=search) |
            Q(name__icontains=search) |
            Q(phone__icontains=search)
        )
    
    # Statistics for this type
    total_count = PCMember.objects.filter(member_type=member_type).count()
    active_count = PCMember.objects.filter(member_type=member_type, is_active=True).count()
    total_commission = PCTransaction.objects.filter(pc_member__member_type=member_type).aggregate(
        Sum('commission_amount'))['commission_amount__sum'] or 0
    
    # Get display name and commission percentage
    type_info = {
        'GENERAL': {'name': 'General', 'percentage': 30, 'color': 'secondary'},
        'LIFETIME': {'name': 'Lifetime', 'percentage': 35, 'color': 'primary'},
        'PREMIUM': {'name': 'Premium', 'percentage': 50, 'color': 'success'},
    }
    
    context = {
        'members': members,
        'member_type': member_type,
        'type_info': type_info[member_type],
        'search': search,
        'total_count': total_count,
        'active_count': active_count,
        'total_commission': total_commission,
    }
    
    return render(request, 'accounts/pc_member_list.html', context)


@login_required
def pc_member_create(request):
    """Create new PC member (Admin only)"""
    if not request.user.is_admin:
        messages.error(request, "Access denied. Admin only.")
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        # Debug logging
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            # Get form data
            member_type = request.POST.get('member_type', '').strip().upper()
            name = request.POST.get('name', '').strip()
            phone = request.POST.get('phone', '').strip()
            email = request.POST.get('email', '').strip()
            address = request.POST.get('address', '').strip()
            notes = request.POST.get('notes', '').strip()
            is_active = request.POST.get('is_active') == 'on'  # Checkbox value
            
            logger.info(f"PC Member Creation - Type: {member_type}, Name: {name}, Phone: {phone}, Active: {is_active}")
            
            # Validate required fields
            errors = []
            if not name:
                errors.append("Name is required")
            if not phone:
                errors.append("Phone number is required")
            if not member_type:
                errors.append("Member type is required")
            
            # Validate member type
            valid_types = ['GENERAL', 'LIFETIME', 'PREMIUM']
            if member_type and member_type not in valid_types:
                errors.append(f"Invalid member type. Must be one of: {', '.join(valid_types)}")
            
            # Check for duplicate phone
            if phone and PCMember.objects.filter(phone=phone).exists():
                errors.append(f"Phone number {phone} is already registered")
            
            # If there are errors, show them and redirect
            if errors:
                for error in errors:
                    messages.error(request, error)
                return redirect('accounts:pc_member_create')
            
            # Set default commission rates based on member type
            commission_rates = {
                'GENERAL': {'normal': 15.00, 'digital': 20.00, 'other': 15.00},
                'LIFETIME': {'normal': 20.00, 'digital': 25.00, 'other': 20.00},
                'PREMIUM': {'normal': 25.00, 'digital': 30.00, 'other': 25.00},
            }
            
            rates = commission_rates.get(member_type, commission_rates['GENERAL'])
            
            # Create PC member
            member = PCMember.objects.create(
                member_type=member_type,
                name=name,
                phone=phone,
                email=email,
                address=address,
                commission_percentage=rates['other'],
                normal_test_commission=rates['normal'],
                digital_test_commission=rates['digital'],
                notes=notes,
                is_active=is_active,
                created_by=request.user
            )
            
            logger.info(f"✅ PC Member created: {member.pc_code} - {member.name}")
            
            messages.success(
                request,
                f'✅ PC Member created successfully!<br>'
                f'Code: <strong>{member.pc_code}</strong><br>'
                f'Name: {member.name}<br>'
                f'Type: {member.get_member_type_display()}<br>'
                f'Commission: Normal {rates["normal"]}%, Digital {rates["digital"]}%',
                extra_tags='safe'
            )
            return redirect('accounts:pc_dashboard')
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            messages.error(request, f"Error creating PC member: {str(e)}")
            # Log the full error for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"PC Member creation error: {error_details}")
            return redirect('accounts:pc_member_create')
    
    # GET request - show form
    default_commissions = {
        'GENERAL': {'normal': 15.00, 'digital': 20.00, 'other': 15.00},
        'LIFETIME': {'normal': 20.00, 'digital': 25.00, 'other': 20.00},
        'PREMIUM': {'normal': 25.00, 'digital': 30.00, 'other': 25.00},
    }
    
    context = {
        'default_commissions': default_commissions,
    }
    
    return render(request, 'accounts/pc_member_create.html', context)


@login_required
def pc_member_detail(request, pc_code):
    """View PC member details and transactions"""
    if not request.user.is_admin:
        messages.error(request, "Access denied. Admin only.")
        return redirect('accounts:dashboard')
    
    member = get_object_or_404(PCMember, pc_code=pc_code)
    
    # Get transactions
    transactions = member.transactions.all()[:50]  # Last 50 transactions
    
    # Statistics
    today = timezone.now().date()
    stats = {
        'today_transactions': member.transactions.filter(transaction_date__date=today).count(),
        'today_commission': member.transactions.filter(transaction_date__date=today).aggregate(
            Sum('commission_amount'))['commission_amount__sum'] or 0,
        'month_transactions': member.transactions.filter(
            transaction_date__month=today.month, 
            transaction_date__year=today.year
        ).count(),
        'month_commission': member.transactions.filter(
            transaction_date__month=today.month, 
            transaction_date__year=today.year
        ).aggregate(Sum('commission_amount'))['commission_amount__sum'] or 0,
        'unpaid_commission': member.transactions.filter(is_paid_to_member=False).aggregate(
            Sum('commission_amount'))['commission_amount__sum'] or 0,
    }
    
    context = {
        'member': member,
        'transactions': transactions,
        'stats': stats,
    }
    
    return render(request, 'accounts/pc_member_detail.html', context)


@login_required
def pc_transaction_create(request):
    """Create PC transaction (Receptionist)"""
    if not request.user.is_receptionist and not request.user.is_admin:
        messages.error(request, "Access denied. Receptionist/Admin only.")
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        pc_code = request.POST.get('pc_code')
        total_amount = float(request.POST.get('total_amount', 0))
        patient_id = request.POST.get('patient_id', '')
        appointment_id = request.POST.get('appointment_id', '')
        notes = request.POST.get('notes', '')
        
        # Find PC member
        try:
            member = PCMember.objects.get(pc_code=pc_code, is_active=True)
        except PCMember.DoesNotExist:
            messages.error(request, f'PC Code "{pc_code}" not found or inactive.')
            return redirect('accounts:pc_transaction_create')
        
        # Get patient and appointment if provided
        patient = Patient.objects.filter(patient_id=patient_id).first() if patient_id else None
        appointment = Appointment.objects.filter(id=appointment_id).first() if appointment_id else None
        
        # Create transaction
        transaction = PCTransaction.objects.create(
            pc_member=member,
            patient=patient,
            appointment=appointment,
            total_amount=total_amount,
            commission_percentage=member.commission_percentage,
            recorded_by=request.user,
            notes=notes
        )
        
        messages.success(request, 
            f'Transaction recorded! PC: ৳{transaction.commission_amount:.2f}, Admin: ৳{transaction.admin_amount:.2f}')
        return redirect('accounts:receptionist_dashboard')
    
    # Get recent patients for easy selection
    recent_patients = Patient.objects.all().order_by('-registered_at')[:20]
    
    context = {
        'recent_patients': recent_patients,
    }
    
    return render(request, 'accounts/pc_transaction_create.html', context)


@login_required
def pc_dashboard(request):
    """PC System Dashboard (Admin only)"""
    if not request.user.is_admin:
        messages.error(request, "Access denied. Admin only.")
        return redirect('accounts:dashboard')
    
    today = timezone.now().date()
    this_month_start = today.replace(day=1)
    
    # Overall statistics
    total_members = PCMember.objects.filter(is_active=True).count()
    total_transactions = PCTransaction.objects.count()
    total_commission_paid = PCTransaction.objects.aggregate(
        Sum('commission_amount'))['commission_amount__sum'] or 0
    total_admin_revenue = PCTransaction.objects.aggregate(
        Sum('admin_amount'))['admin_amount__sum'] or 0
    
    # Today's statistics
    today_transactions = PCTransaction.objects.filter(transaction_date__date=today)
    today_commission = today_transactions.aggregate(Sum('commission_amount'))['commission_amount__sum'] or 0
    today_admin_revenue = today_transactions.aggregate(Sum('admin_amount'))['admin_amount__sum'] or 0
    
    # This month's statistics
    month_transactions = PCTransaction.objects.filter(transaction_date__gte=this_month_start)
    month_commission = month_transactions.aggregate(Sum('commission_amount'))['commission_amount__sum'] or 0
    month_admin_revenue = month_transactions.aggregate(Sum('admin_amount'))['admin_amount__sum'] or 0
    
    # Top performers
    top_members = PCMember.objects.filter(is_active=True).order_by('-total_commission_earned')[:10]
    
    # Recent transactions
    recent_transactions = PCTransaction.objects.all().select_related('pc_member', 'patient')[:20]
    
    # Unpaid commissions
    unpaid_commission = PCTransaction.objects.filter(is_paid_to_member=False).aggregate(
        Sum('commission_amount'))['commission_amount__sum'] or 0
    
    # By member type
    general_stats = {
        'count': PCMember.objects.filter(member_type='GENERAL', is_active=True).count(),
        'commission': PCTransaction.objects.filter(pc_member__member_type='GENERAL').aggregate(
            Sum('commission_amount'))['commission_amount__sum'] or 0,
    }
    lifetime_stats = {
        'count': PCMember.objects.filter(member_type='LIFETIME', is_active=True).count(),
        'commission': PCTransaction.objects.filter(pc_member__member_type='LIFETIME').aggregate(
            Sum('commission_amount'))['commission_amount__sum'] or 0,
    }
    investor_stats = {
        'count': PCMember.objects.filter(member_type='PREMIUM', is_active=True).count(),
        'commission': PCTransaction.objects.filter(pc_member__member_type='PREMIUM').aggregate(
            Sum('commission_amount'))['commission_amount__sum'] or 0,
    }
    
    # Get default rates for each member type (from first member of each type or defaults)
    general_rates = PCMember.objects.filter(member_type='GENERAL').first()
    lifetime_rates = PCMember.objects.filter(member_type='LIFETIME').first()
    premium_rates = PCMember.objects.filter(member_type='PREMIUM').first()
    
    context = {
        'total_members': total_members,
        'total_transactions': total_transactions,
        'total_commission': total_commission_paid,
        'admin_revenue': total_admin_revenue,
        'today_transactions': today_transactions.count(),
        'today_commission': today_commission,
        'today_admin_revenue': today_admin_revenue,
        'month_transactions_count': month_transactions.count(),
        'month_commission': month_commission,
        'month_admin_revenue': month_admin_revenue,
        'top_members': top_members,
        'recent_transactions': recent_transactions,
        'unpaid_commission': unpaid_commission,
        'general_count': general_stats['count'],
        'general_commission': general_stats['commission'],
        'lifetime_count': lifetime_stats['count'],
        'lifetime_commission': lifetime_stats['commission'],
        'investor_count': investor_stats['count'],
        'investor_commission': investor_stats['commission'],
        'general_rates': general_rates,
        'lifetime_rates': lifetime_rates,
        'premium_rates': premium_rates,
    }
    
    return render(request, 'accounts/pc_dashboard.html', context)


@login_required
def pc_lookup_api(request):
    """API endpoint to lookup PC member by code"""
    from django.http import JsonResponse
    
    pc_code = request.GET.get('code', '').strip()
    
    if not pc_code:
        return JsonResponse({'success': False, 'error': 'No code provided'})
    
    try:
        member = PCMember.objects.get(pc_code=pc_code, is_active=True)
        return JsonResponse({
            'success': True,
            'pc_code': member.pc_code,
            'name': member.name,
            'member_type': member.get_member_type_display(),
            'phone': member.phone,
            'commission_percentage': float(member.commission_percentage),
            'total_earned': float(member.total_commission_earned),
            'due_amount': float(member.due_amount),
            # Legacy support
            'member': {
                'id': member.pk,
                'name': member.name,
                'pc_code': member.pc_code,
                'type': member.get_member_type_display(),
                'phone': member.phone,
                'commission': float(member.commission_percentage),
                'total': float(member.total_commission_earned),
            }
        })
    except PCMember.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'PC member not found or inactive'})


@login_required
def pc_mark_paid(request, pc_code):
    """Mark all unpaid commissions as paid for a PC member (Admin only)"""
    if not request.user.is_admin:
        messages.error(request, "Access denied. Admin only.")
        return redirect('accounts:dashboard')
    
    member = get_object_or_404(PCMember, pc_code=pc_code)
    
    # Check if there's any due amount
    if member.due_amount <= 0:
        messages.info(request, f'No unpaid commissions for {member.name}.')
        return redirect('accounts:pc_member_list', member_type=member.member_type)
    
    # Get all unpaid transactions
    unpaid_transactions = PCTransaction.objects.filter(
        pc_member=member,
        is_paid_to_member=False
    )
    
    unpaid_count = unpaid_transactions.count()
    due_amount = float(member.due_amount)
    
    # Mark all as paid
    unpaid_transactions.update(
        is_paid_to_member=True,
        paid_at=timezone.now()
    )
    
    # Move due amount to total earned
    member.total_commission_earned += member.due_amount
    member.due_amount = 0
    member.save()
    
    messages.success(
        request, 
        f'Payment confirmed! ৳{due_amount:.2f} paid to {member.name} ({unpaid_count} transactions marked as paid).'
    )
    
    # Redirect back to the member list of the same type
    return redirect('accounts:pc_member_list', member_type=member.member_type)


@login_required
def pc_member_delete(request, pc_code):
    """Delete PC member (Admin only) - Now allows deletion even with transactions"""
    if not request.user.is_admin:
        messages.error(request, "Access denied. Admin only.")
        return redirect('accounts:dashboard')
    
    member = get_object_or_404(PCMember, pc_code=pc_code)
    member_type = member.member_type
    member_name = member.name
    
    # Check member status
    transaction_count = member.transactions.count()
    has_due_amount = member.due_amount > 0
    total_earned = member.total_commission_earned
    
    if request.method == 'POST':
        # Always permanently delete (user requested this behavior)
        member.delete()
        
        # Build deletion info message
        info_parts = []
        if transaction_count > 0:
            info_parts.append(f'{transaction_count} transaction(s)')
        if has_due_amount:
            info_parts.append(f'৳{member.due_amount:.2f} unpaid commission')
        if total_earned > 0:
            info_parts.append(f'৳{total_earned:.2f} total earned')
        
        info_text = ' - ' + ', '.join(info_parts) if info_parts else ''
        
        messages.success(
            request,
            f'✅ PC Member "{member_name}" ({pc_code}) has been permanently deleted.{info_text}',
            extra_tags='safe'
        )
        
        return redirect('accounts:pc_member_list', member_type=member_type)
    
    # Show confirmation page
    context = {
        'member': member,
        'transaction_count': transaction_count,
        'has_transactions': transaction_count > 0,
        'has_due_amount': has_due_amount,
        'total_earned': total_earned,
    }
    
    return render(request, 'accounts/pc_member_delete_confirm.html', context)

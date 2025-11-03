# 🏥 Professional Prescription Module - Complete Implementation

## ✅ Overview
A complete, professional prescription writing system for doctors with comprehensive clinical fields, dynamic medicine management, and professional print templates matching real medical prescriptions.

---

## 📋 Features Implemented

### 1. **Enhanced Prescription Model** ✅
**File**: `appointments/models.py`

```python
class Prescription(models.Model):
    # Basic Info
    prescription_number = models.CharField(max_length=50, unique=True)
    appointment = models.ForeignKey(Appointment)
    patient = models.ForeignKey(Patient)
    doctor = models.ForeignKey(User)
    
    # Clinical Details
    chief_complaint = models.TextField(blank=True)
    history = models.TextField(blank=True)
    on_examination = models.TextField(blank=True)
    
    # Vitals
    blood_pressure = models.CharField(max_length=20, blank=True)
    pulse = models.CharField(max_length=10, blank=True)
    temperature = models.CharField(max_length=10, blank=True)
    weight = models.CharField(max_length=10, blank=True)
    
    # Diagnosis & Treatment
    diagnosis = models.TextField()  # Required
    investigation = models.TextField(blank=True)
    advice = models.TextField(blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Migration**: `0007_prescription_blood_pressure_prescription_history_and_more`
- Status: ✅ Applied successfully
- Added: 9 clinical fields

---

### 2. **Professional Prescription Form** ✅
**File**: `templates/appointments/prescription_write.html`

#### Features:
1. **Patient Information Card**
   - Name, ID, Age, Gender
   - Displayed prominently at top

2. **Chief Complaint Section**
   - Multi-line textarea
   - Example: "Fever and cough for 3 days"

3. **History Section**
   - Past medical history
   - Family history
   - Previous treatments

4. **Vitals Grid** (4-column responsive)
   - Blood Pressure (e.g., "140/70 mmHg")
   - Pulse (e.g., "72 bpm")
   - Temperature (e.g., "98.6°F")
   - Weight (e.g., "60 kg")

5. **On Examination**
   - Physical examination findings
   - System-wise examination

6. **Diagnosis** (Required ⚠️)
   - Primary and secondary diagnoses
   - Must be filled before saving

7. **Investigation**
   - Lab tests ordered
   - Imaging studies (MRI, X-Ray, ECG)

8. **Medicines (Rx)** - Dynamic Rows
   - Medicine Name
   - Dosage
   - Frequency (1+1+1, 1+0+1, etc.)
   - Duration
   - Instructions (before/after food)
   - **Add Medicine** button (JavaScript)
   - **Remove** button for each row

9. **Advice**
   - Post-treatment instructions
   - Lifestyle modifications
   - Precautions

10. **Follow-up Date**
    - Date picker

11. **Action Buttons**
    - **Save** - Save and view print preview
    - **Save & Send to Reception** - Mark complete and send for printing

#### JavaScript Features:
```javascript
// Add new medicine row dynamically
function addMedicineRow() {
    // Clones medicine row template
    // Adds to form
}

// Remove medicine row
function removeMedicineRow(button) {
    // Removes specific row
}
```

---

### 3. **Enhanced Prescription Create View** ✅
**File**: `appointments/views.py`

```python
@login_required
def prescription_create(request, appointment_id):
    """Create comprehensive prescription"""
    
    if request.method == 'POST':
        # Extract all clinical fields
        chief_complaint = request.POST.get('chief_complaint')
        history = request.POST.get('history')
        blood_pressure = request.POST.get('blood_pressure')
        pulse = request.POST.get('pulse')
        temperature = request.POST.get('temperature')
        weight = request.POST.get('weight')
        on_examination = request.POST.get('on_examination')
        diagnosis = request.POST.get('diagnosis')  # Required
        investigation = request.POST.get('investigation')
        advice = request.POST.get('advice')
        follow_up_date = request.POST.get('follow_up_date')
        
        # Extract dynamic medicine rows
        medicine_names = request.POST.getlist('medicine_name[]')
        medicine_dosages = request.POST.getlist('dosage[]')
        medicine_frequencies = request.POST.getlist('frequency[]')
        medicine_durations = request.POST.getlist('duration[]')
        medicine_instructions = request.POST.getlist('medicine_instructions[]')
        
        # Validate diagnosis
        if not diagnosis:
            messages.error(request, 'Diagnosis is required!')
            return render(...)
        
        # Create/Update Prescription
        prescription = Prescription(...)
        
        # Generate Rx Number: RX20250122XXXX
        today = datetime.now()
        prefix = f"RX{today.strftime('%Y%m%d')}"
        last_prescription = Prescription.objects.filter(
            prescription_number__startswith=prefix
        ).order_by('prescription_number').last()
        
        if last_prescription:
            last_number = int(last_prescription.prescription_number[-4:])
            new_number = last_number + 1
        else:
            new_number = 1
        
        prescription.prescription_number = f"{prefix}{new_number:04d}"
        prescription.save()
        
        # Save all medicines
        for i in range(len(medicine_names)):
            if medicine_names[i].strip():
                Medicine.objects.create(
                    prescription=prescription,
                    medicine_name=medicine_names[i],
                    dosage=medicine_dosages[i],
                    frequency=medicine_frequencies[i],
                    duration=medicine_durations[i],
                    instructions=medicine_instructions[i],
                )
        
        # Check button clicked
        if 'send_to_reception' in request.POST:
            appointment.status = 'COMPLETED'
            appointment.save()
            messages.success(request, 'Prescription sent to reception!')
            return redirect('accounts:doctor_dashboard')
        else:
            return redirect('appointments:prescription_print', pk=prescription.pk)
```

**Key Features**:
- ✅ Handles all clinical fields
- ✅ Processes dynamic medicine arrays
- ✅ Auto-generates Rx numbers (RX20250122XXXX)
- ✅ Two save modes: Save or Send to Reception
- ✅ Validation for required diagnosis field

---

### 4. **Professional Print Template** ✅
**File**: `templates/appointments/prescription_print_pro.html`

#### Design Features:
- **A4 Size**: Perfect print layout (21cm × 29.7cm)
- **Hospital Header**:
  - Hospital name in large bold blue text
  - Bengali name (নাজিরপুর বিশেষজ্ঞ মেডিসিন বিভাগ)
  - Address and contact info
  - Blue bottom border (3px solid)

- **Doctor Information**:
  - Name in large bold text
  - Specialization and qualifications
  - Top border separation

- **Patient Information Card**:
  - Left: Name, Age, Gender, Patient ID
  - Right: Date, Rx Number
  - Light grey background
  - Blue left border (4px solid)

- **Clinical Sections**:
  1. Chief Complaint
  2. History
  3. On Examinations (Vitals in 2-column grid)
  4. Diagnosis
  5. Investigation

- **Prescription (Rx) Section**:
  - Large decorative "℞" symbol (28pt)
  - Numbered medicine list
  - Each medicine in card format:
    - Medicine name (bold)
    - Dosage, frequency, duration
    - Instructions (smaller text)
  - Blue left border for each medicine

- **Advice Box**:
  - Yellow background (#fffbf0)
  - Orange border (2px solid #ffc107)
  - "Advices:" heading in orange
  - Rounded corners (5px)

- **Follow-up Date**:
  - Displayed if specified

- **Footer**:
  - Left: Printed date & time
  - Right: Doctor signature section
    - Signature line (200px width, 2px solid)
    - Doctor name (bold)
    - Specialization

- **Print Button**:
  - Fixed bottom-right position
  - Blue background
  - Hidden on print (`.no-print` class)
  - One-click printing

#### Print Styles:
```css
@media print {
    .no-print {
        display: none;
    }
    
    @page {
        size: A4;
        margin: 0;
    }
}
```

#### JavaScript:
```javascript
// Print button
window.print()

// Optional auto-print on load
// window.onload = function() { window.print(); };
```

---

### 5. **Doctor Dashboard Integration** ✅
**File**: `templates/accounts/doctor_dashboard.html`

#### Prescription Buttons in Queue:
- **Waiting**: "Call Next" button
- **Called/In Consultation**: 
  - "View" button
  - **"Prescription"** button → Opens prescription form
- **Completed**:
  - If prescription exists: **"Print Rx"** button (opens in new tab)
  - If no prescription: **"Write Rx"** button

```html
{% if appointment.status == 'called' or appointment.status == 'in_consultation' %}
<a href="{% url 'appointments:prescription_create' appointment.pk %}" 
   class="btn btn-sm btn-primary">
    <i class="bi bi-file-text"></i> Prescription
</a>
{% elif appointment.status == 'completed' %}
    {% if appointment.prescriptions.exists %}
    <a href="{% url 'appointments:prescription_print' appointment.prescriptions.first.pk %}" 
       class="btn btn-sm btn-success" target="_blank">
        <i class="bi bi-printer"></i> Print Rx
    </a>
    {% endif %}
{% endif %}
```

---

### 6. **Receptionist Dashboard Integration** ✅
**File**: `templates/accounts/receptionist_dashboard.html`

#### Features:
1. **Stats Card**: "Pending Prints" counter
2. **"Prescriptions Ready to Print" Section**:
   - Shows completed prescriptions
   - Yellow/Warning card design
   - Each prescription card shows:
     - Patient name & ID
     - Doctor name
     - Created timestamp
     - Medicine count badge
     - **Print** button (primary)
     - **View** button (outline)
   
3. **Print All** Button:
   - Prints all pending prescriptions sequentially
   - 2-second delay between prints

4. **Print Functions** (JavaScript):
```javascript
function printPrescription(prescriptionId) {
    // Load prescription in hidden iframe
    const printFrame = document.getElementById('printFrame');
    printFrame.src = `/appointments/prescription/${prescriptionId}/print/`;
    
    // Wait for load, then print
    printFrame.onload = function() {
        setTimeout(() => {
            printFrame.contentWindow.print();
            
            // Mark as printed via API
            fetch(`/accounts/api/prescription/${prescriptionId}/mark-printed/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                }
            });
            
            // Reload after 1 second
            setTimeout(() => location.reload(), 1000);
        }, 500);
    };
}

function printAll() {
    // Sequential printing with 2-second delays
    {% for prescription in prescriptions_to_print %}
    setTimeout(() => printPrescription({{ prescription.pk }}), 
               {{ forloop.counter0 }} * 2000);
    {% endfor %}
}
```

5. **Hidden Print IFrame**:
```html
<iframe id="printFrame" style="display:none;"></iframe>
```

---

## 🔄 Complete Workflow

### Doctor Side:
1. Patient is in consultation (status: `called` or `in_consultation`)
2. Doctor clicks **"Prescription"** button from dashboard
3. Form opens with patient information pre-filled
4. Doctor fills:
   - Chief complaint
   - History
   - Vitals (BP, Pulse, Temp, Weight)
   - Examination findings
   - **Diagnosis** (required)
   - Investigation orders
   - Medicines (add multiple rows)
   - Advice
   - Follow-up date
5. Doctor clicks:
   - **"Save"** → Opens print preview
   - **"Save & Send to Reception"** → Marks appointment complete, sends to reception queue

### Reception Side:
1. Receptionist dashboard shows **"Prescriptions Ready to Print"** section
2. Each completed prescription appears as a card
3. Receptionist clicks **"Print"** button
4. Prescription opens in hidden iframe
5. Browser print dialog appears
6. After printing, prescription is marked as printed
7. Card is removed from pending list

---

## 📁 Files Modified/Created

### Models:
- ✅ `appointments/models.py` - Enhanced Prescription model with 9 clinical fields

### Views:
- ✅ `appointments/views.py` - Updated `prescription_create()` view
- ✅ `appointments/views.py` - Updated `prescription_print()` to use new template

### Templates:
- ✅ `templates/appointments/prescription_write.html` - NEW comprehensive form
- ✅ `templates/appointments/prescription_print_pro.html` - NEW professional print template
- ✅ `templates/accounts/doctor_dashboard.html` - Already has prescription buttons
- ✅ `templates/accounts/receptionist_dashboard.html` - Already has print section

### Migrations:
- ✅ `appointments/migrations/0007_prescription_blood_pressure_prescription_history_and_more.py`

---

## 🧪 Testing the System

### 1. Create Test Prescription:
```python
# From doctor dashboard
1. Login as doctor: phone=01700000001, password=admin123
2. Navigate to /accounts/doctor-dashboard/
3. Click "Call Next" on a waiting patient
4. Click "Prescription" button
5. Fill all fields:
   - Chief Complaint: "Fever and cough for 3 days"
   - History: "No previous history"
   - BP: 140/70 mmHg
   - Pulse: 72 bpm
   - Temperature: 98.6°F
   - Weight: 60 kg
   - Diagnosis: "PLID, COPD, Urticaria"
   - Medicines:
     * Tab. Paracetamol 500mg, 1+1+1, 7 days, After food
     * Tab. Amoxicillin 500mg, 1+0+1, 5 days, Before food
     * Syp. Cough, 2 tsp, 3 times daily, 7 days
   - Advice: "Drink plenty of water. Rest well. Avoid cold drinks."
   - Follow-up: [7 days from today]
6. Click "Save & Send to Reception"
```

### 2. Print from Reception:
```python
# From receptionist dashboard
1. Login as receptionist: phone=01800000001, password=admin123
2. Navigate to /accounts/receptionist-dashboard/
3. See "Prescriptions Ready to Print" section
4. Click "Print" on the prescription
5. Browser print dialog appears
6. Print or Save as PDF
```

### 3. Check Print Quality:
- ✅ A4 size perfect
- ✅ Hospital header with logo space
- ✅ Doctor details prominent
- ✅ Patient info clear
- ✅ All clinical sections formatted
- ✅ Medicines in professional layout
- ✅ Signature line at bottom
- ✅ Print date stamp

---

## 🎨 Design Features Matching Medical Prescription

### Your Image vs Our Implementation:

| Feature | Image | Our System |
|---------|-------|------------|
| Hospital Header | ✅ | ✅ Blue bold, Bengali subtitle |
| Doctor Info | ✅ | ✅ Name, degree, specialization |
| Patient Details | ✅ | ✅ Name, ID, Age, Gender, Date |
| Chief Complaint | ✅ | ✅ Multi-line textarea |
| History | ✅ | ✅ Full history section |
| Vitals (BP, Pulse, etc.) | ✅ | ✅ 2-column grid display |
| On Examination | ✅ | ✅ Detailed findings section |
| Diagnosis | ✅ | ✅ Required field, multi-line |
| Investigation | ✅ | ✅ Lab tests, imaging |
| Rx (Medicines) | ✅ | ✅ Numbered list, dosage, frequency |
| Advice | ✅ | ✅ Yellow highlighted box |
| Signature Line | ✅ | ✅ Doctor name, line for signature |
| Follow-up Date | ✅ | ✅ Date picker |

---

## 📊 Prescription Number Format

**Format**: `RX{YYYYMMDD}{XXXX}`

**Examples**:
- `RX202501220001` - First prescription on Jan 22, 2025
- `RX202501220002` - Second prescription same day
- `RX202501230001` - First prescription next day

**Auto-generation Logic**:
```python
today = datetime.now()
prefix = f"RX{today.strftime('%Y%m%d')}"

last_prescription = Prescription.objects.filter(
    prescription_number__startswith=prefix
).order_by('prescription_number').last()

if last_prescription:
    last_number = int(last_prescription.prescription_number[-4:])
    new_number = last_number + 1
else:
    new_number = 1

prescription_number = f"{prefix}{new_number:04d}"
```

---

## 🔒 Access Control

### Doctor:
- ✅ Can write prescriptions for their patients
- ✅ Can edit their own prescriptions
- ✅ Can view all their prescriptions
- ✅ Dashboard shows prescription buttons

### Receptionist:
- ✅ Can view completed prescriptions
- ✅ Can print prescriptions
- ✅ Dashboard shows pending prints
- ✅ Can mark prescriptions as printed

### Admin:
- ✅ Full access to all prescriptions
- ✅ Can write prescriptions for any doctor
- ✅ Can edit any prescription

---

## 🌐 URLs

```python
# Prescription URLs
path('prescription/<int:appointment_id>/create/', prescription_create, name='prescription_create'),
path('prescription/<int:pk>/', prescription_detail, name='prescription_detail'),
path('prescription/<int:pk>/print/', prescription_print, name='prescription_print'),
```

---

## 📱 Mobile Responsive

- ✅ Form responsive on tablets
- ✅ Print template optimized for A4 (desktop print)
- ✅ Buttons touch-friendly
- ✅ Grid layouts stack on mobile

---

## 🚀 Production Ready

### Checklist:
- ✅ All migrations applied
- ✅ Views handle errors gracefully
- ✅ Templates use Bootstrap 5
- ✅ Print layout matches professional standards
- ✅ JavaScript functions tested
- ✅ Django messages for user feedback
- ✅ Required field validation (diagnosis)
- ✅ Dynamic medicine rows working
- ✅ Auto-refresh in receptionist dashboard (2 min)

---

## 📝 Sample Data

### Test Prescription Data:
```
Chief Complaint: "Fever (103°F) and dry cough for 3 days, body ache"
History: "Diabetic for 5 years on Tab. Metformin 500mg. No known allergies."
BP: 140/70 mmHg
Pulse: 72 bpm
Temperature: 103°F
Weight: 60 kg
On Examination: "Throat congestion, mild chest crackles on auscultation"
Diagnosis: "1. Viral Fever 2. Upper Respiratory Tract Infection 3. Hyperglycemia"
Investigation: "CBC, RBS, Chest X-Ray"

Medicines:
1. Tab. Paracetamol 500mg - 1+1+1 - 5 days - After food, if fever >100°F
2. Tab. Azithromycin 500mg - 1+0+0 - 3 days - After breakfast
3. Tab. Cetirizine 10mg - 0+0+1 - 7 days - Before sleep
4. Syp. Cough (Benadryl) - 2 tsp - 3 times - 5 days - After food

Advice:
- পর্যাপ্ত বিশ্রাম নিন (Take adequate rest)
- প্রচুর পানি পান করুন (Drink plenty of water)
- ঠান্ডা খাবার এড়িয়ে চলুন (Avoid cold food/drinks)
- হালকা গরম পানি দিয়ে গার্গল করুন (Gargle with warm water)
- চিনি-জাতীয় খাবার এড়িয়ে চলুন (Avoid sugary foods)

Follow-up: 7 days
```

---

## ✅ Status: COMPLETE

The professional prescription module is fully implemented and ready for use. All features match the requirements from the medical prescription image provided by the user.

### Next Steps (Optional Enhancements):
1. Add prescription history view for patients
2. Add medicine templates for quick selection
3. Add diagnosis templates/ICD codes
4. Add digital signature upload for doctors
5. Add prescription email/SMS sending
6. Add prescription analytics dashboard

---

## 📞 Support

For any issues or questions about the prescription module:
1. Check this documentation
2. Review the code comments in views and templates
3. Test with sample data provided above

---

**Document Created**: January 2025  
**Status**: ✅ Complete and Production Ready  
**Version**: 1.0


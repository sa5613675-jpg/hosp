# VPS Deployment Commands - Ready to Deploy

## 🚀 Quick Deploy (Run these commands on your VPS)

### Step 1: Connect to VPS
```bash
ssh root@your-vps-ip
```

### Step 2: Navigate to Project Directory
```bash
cd /root/hosp
```

### Step 3: Pull Latest Changes from GitHub
```bash
git pull origin main
```

### Step 4: Activate Virtual Environment
```bash
source venv/bin/activate
```

### Step 5: Install/Update Dependencies
```bash
pip install -r requirements.txt
```

### Step 6: Run Database Migrations
```bash
python manage.py migrate
```

### Step 7: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 8: Restart Services
```bash
sudo systemctl restart hosp
sudo systemctl restart nginx
```

### Step 9: Check Service Status
```bash
sudo systemctl status hosp
sudo systemctl status nginx
```

---

## 📋 What's New in This Update

### ✅ PC Member System
- **6-digit PC codes**: 100001 (GENERAL), 200001 (LIFETIME), 300001 (PREMIUM)
- **Delete functionality**: Safe deletion with transaction checking
- **Fixed commission updates**: Proper Decimal conversion
- **PREMIUM member type**: Renamed from INVESTOR

### ✅ Lab System
- **Simplified workflow**: Payment → Order → Voucher (no sample collection)
- **Correct commission logic**: Admin gets proper share after PC commission
- **Updated voucher**: Professional template with hospital branding

### ✅ Doctor Consultation
- **Important**: Consultation fees NO LONGER go to admin account
- Fees belong to doctor and reception only

### ✅ Contact Updates
- **Phone**: 01332-856002 (all public pages)
- **Hospital**: Universal Health Services & Diagnostic Center
- **Address**: Removed পৌরসদ from all locations

---

## 🔍 Verify Deployment

After deployment, check these URLs:

1. **Homepage**: http://your-vps-ip/
2. **Admin Login**: http://your-vps-ip/accounts/login/
3. **PC Dashboard**: http://your-vps-ip/accounts/pc-dashboard/
4. **Lab Orders**: http://your-vps-ip/lab/orders/

---

## ⚠️ Important Notes

### Database Migrations
Two new migrations will be applied:
- `accounts/0011_alter_pcmember_commission_percentage_and_more.py`
- `lab/0002_remove_laborder_pc_member_laborder_pc_code.py`

### New Templates
- `templates/accounts/pc_member_delete_confirm.html`
- `templates/lab/lab_order_form_simple.html`

### Modified Features
- PC member deletion (admin only)
- Lab order creation (simplified)
- Commission calculation (corrected)
- Contact information (updated)

---

## 🐛 Troubleshooting

### If service doesn't start:
```bash
# Check logs
sudo journalctl -u hosp -n 50

# Check nginx logs
sudo tail -f /var/log/nginx/error.log
```

### If migrations fail:
```bash
# Check migration status
python manage.py showmigrations

# Try running migrations individually
python manage.py migrate accounts
python manage.py migrate lab
```

### If static files don't load:
```bash
# Check static files path
python manage.py findstatic admin/css/base.css

# Ensure nginx can access static files
sudo chmod -R 755 /root/hosp/staticfiles/
```

---

## 📞 Production Credentials

**Admin Account:**
- Username: `01332856000`
- Password: `856000`

**Public Helpline:**
- Phone: `01332-856002`

---

## ✨ Testing Checklist

After deployment, test:

- [ ] Login as admin
- [ ] Create new PC member (verify 6-digit code)
- [ ] Update PC commission rates
- [ ] Delete PC member (test both with/without transactions)
- [ ] Create lab order with PC code
- [ ] Print lab voucher (check hospital name & phone)
- [ ] Create doctor appointment (verify no admin income recorded)
- [ ] Check landing page (verify new phone number)

---

## 🔄 One-Line Deploy Command

```bash
cd /root/hosp && source venv/bin/activate && git pull origin main && pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput && sudo systemctl restart hosp && sudo systemctl restart nginx && sudo systemctl status hosp
```

---

**Deployment Date**: November 14, 2025  
**Commit**: 2a65056  
**Status**: ✅ Ready for Production

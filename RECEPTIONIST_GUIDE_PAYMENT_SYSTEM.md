# 🏥 RECEPTIONIST QUICK GUIDE - Appointment Booking with Payment

## 📋 Quick Reference Card

```
┌────────────────────────────────────────────────┐
│  RECEPTIONIST LOGIN CREDENTIALS                │
├────────────────────────────────────────────────┤
│  Username:  reception                          │
│  Password:  123456                             │
│  URL:       http://localhost:8000              │
└────────────────────────────────────────────────┘
```

---

## 🚀 Step-by-Step: Book Appointment with Payment

### STEP 1️⃣: Check if Patient Exists
- Look for patient in dropdown
- If NOT found → Click "Register New Patient" link
- If found → Continue to Step 2

### STEP 2️⃣: Fill Appointment Form
```
┌─────────────────────────────────────┐
│ 1. Select Patient: [Dropdown ▼]    │
│    Example: রফিকুল ইসলাম - 017...  │
├─────────────────────────────────────┤
│ 2. Select Doctor: [Dropdown ▼]     │
│    Example: Dr. আয়েশা ছিদ্দিকা    │
├─────────────────────────────────────┤
│ 3. Reason for Visit: (Optional)    │
│    [Type reason here...]            │
├─────────────────────────────────────┤
│ 4. Consultation Fee: 300.00 ৳      │
├─────────────────────────────────────┤
│ 5. Payment Method: [Cash ▼]        │
│    - Cash                           │
│    - bKash                          │
│    - Nagad                          │
│    - Rocket                         │
│    - Card                           │
│    - Bank Transfer                  │
└─────────────────────────────────────┘
```

### STEP 3️⃣: Submit & Collect Payment
- Click **"Book Appointment & Collect Payment"** button
- Collect payment from patient
- Give them their serial number

### STEP 4️⃣: Success!
You'll see:
```
✅ Appointment booked! 
Serial #5 for রফিকুল ইসলাম 
Payment: ৳300.00 (CASH)
```

---

## 💡 Important Notes

### ⚠️ Patient Not in List?
If patient is new:
1. Click "Register New Patient" link (opens in new tab)
2. Fill patient registration form
3. Come back to booking page
4. Refresh page (F5)
5. Patient will now appear in dropdown

### 💰 Payment Methods
- **Cash**: For cash payments
- **bKash/Nagad/Rocket**: For mobile payments
- **Card**: For card payments
- **Bank Transfer**: For bank transfers

### 📝 Today's Appointments
Right side shows all today's appointments:
- Grouped by doctor
- Shows serial numbers
- Shows patient status (Waiting/Called/Completed)

---

## 🔍 Common Scenarios

### Scenario 1: Regular Patient Visit
```
Patient: আব্দুল করিম (already registered)
Doctor: Dr. খালিদ হোসেন
Fee: 300৳
Method: Cash

Steps:
1. Select "আব্দুল করিম" from dropdown
2. Select "Dr. খালিদ হোসেন"
3. Leave reason blank (routine checkup)
4. Keep fee at 300৳
5. Select "Cash"
6. Click submit
7. Collect 300৳ cash from patient
8. Tell patient: "Your serial number is #3"
```

### Scenario 2: New Patient (First Time)
```
Patient: New patient named "সাকিব আহমেদ"
Doctor: Dr. আয়েশা ছিদ্দিকা
Fee: 300৳
Method: bKash

Steps:
1. Click "Register New Patient" link
2. Fill registration form with patient details
3. Submit registration
4. Return to booking page (close tab)
5. Refresh booking page
6. Now select "সাকিব আহমেদ" from dropdown
7. Select doctor
8. Enter fee 300৳
9. Select "bKash"
10. Click submit
11. Tell patient to pay via bKash
```

### Scenario 3: Special Fee Patient
```
Patient: ফাতেমা খাতুন
Doctor: Dr. শাকেরা সুলতানা (Cancer Specialist)
Fee: 500৳ (specialist fee)
Method: Cash

Steps:
1. Select patient
2. Select doctor
3. Change fee from 300 to 500
4. Select "Cash"
5. Click submit
6. Collect 500৳ from patient
```

---

## 📊 What You Should See

### Left Side: Booking Form
- Patient dropdown with search
- Doctor dropdown
- Payment fields
- Submit button

### Right Side: Today's Appointments
```
Dr. খালিদ হোসেন          [8 patients]
────────────────────────────────────
Serial  Patient Name    Status    Time
  #1    রফিকুল ইসলাম   Waiting   9:00 AM
  #2    সালমা বেগম      Called    9:15 AM
  #3    মোহাম্মদ রাকিব  Waiting   9:30 AM
```

---

## ✅ Quick Checklist Before Booking

- [ ] Patient exists in dropdown (or registered them first)
- [ ] Selected correct doctor
- [ ] Entered correct consultation fee
- [ ] Selected payment method
- [ ] Ready to collect payment

---

## 🆘 Troubleshooting

### Problem: Patient not in dropdown
**Solution:** Register patient first using "Register New Patient" link

### Problem: Can't submit form
**Solution:** Check all required fields are filled:
- Patient selected ✓
- Doctor selected ✓
- Fee entered ✓
- Payment method selected ✓

### Problem: Wrong serial number shown
**Solution:** This is automatic - each doctor gets their own serial sequence

### Problem: Payment recorded wrong
**Solution:** Contact admin - income records can be edited in finance module

---

## 📞 Need Help?

**Admin Contact:** Ask system administrator

**Emergency:** If system not working, write down:
1. Patient name
2. Doctor name
3. Payment amount & method
4. Time

Admin can manually enter later.

---

## 🎯 Daily End-of-Day Tasks

At end of your shift:
1. Count total cash collected
2. Admin will match with system records
3. System shows your income records automatically

To check your collections:
- Admin can filter Income by "recorded_by" = your username
- Shows all payments you collected today

---

## ⚡ Keyboard Shortcuts

- `Tab`: Move to next field
- `Enter`: Submit form (when on submit button)
- `F5`: Refresh page
- `Ctrl + Click` link: Open in new tab

---

## 📝 Example: Complete Booking Session

**Time: 9:00 AM - First Patient**
```
1. Login at http://localhost:8000
2. Go to "Quick Appointment Booking"
3. Select patient: রফিকুল ইসলাম
4. Select doctor: Dr. খালিদ হোসেন
5. Fee: 300৳
6. Method: Cash
7. Submit → Serial #1 assigned
8. Collect 300৳ cash
9. Tell patient: "Please wait, your serial is #1"
```

**Time: 9:10 AM - Second Patient**
```
1. Select patient: সালমা বেগম
2. Select doctor: Dr. আয়েশা ছিদ্দিকা
3. Fee: 300৳
4. Method: bKash
5. Submit → Serial #1 for this doctor (separate queue)
6. Patient pays via bKash
7. Tell patient: "Serial #1 for Dr. আয়েশা"
```

**Time: 9:15 AM - New Patient**
```
1. Patient says: "First time here"
2. Click "Register New Patient"
3. Fill form: name, age, phone, address, etc.
4. Submit registration
5. Return to booking page
6. Refresh (F5)
7. Patient now in dropdown
8. Continue normal booking
```

---

## 🎉 That's It!

**Remember:**
1. Select patient (register if new)
2. Select doctor
3. Enter fee & payment method
4. Collect payment
5. Give serial number

**Each booking automatically:**
- Creates appointment
- Records payment
- Generates serial number
- Shows on display monitor
- Tracked in admin finance

**Your job done! 🎊**

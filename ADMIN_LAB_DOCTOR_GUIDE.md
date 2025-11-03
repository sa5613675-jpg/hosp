# ✅ Admin Dashboard - Lab Tests & Doctor Details Guide

## 🎯 Status: ALL FEATURES WORKING

Your admin dashboard is fully functional for:
1. ✅ Adding/editing lab test names and prices
2. ✅ Managing doctor details and specializations
3. ✅ Doctor details showing on prescriptions

---

## 🔐 Admin Login

**URL:** http://localhost:8000/admin/

**Admin Accounts:**
- Username: `admin` / Password: `admin123` (or your admin password)
- Username: `01332856000` / Password: (your password)

---

## 1️⃣ How to Add Lab Tests

### Step-by-Step:

1. **Login to Admin Panel**
   - Go to http://localhost:8000/admin/
   - Enter admin username and password

2. **Navigate to Lab Tests**
   ```
   Dashboard → LAB section → Lab tests
   ```

3. **Click "Add Lab Test" Button**
   (Top right corner, green button)

4. **Fill in the Form:**

   **Test Information:**
   - **Test Code:** Unique code (e.g., `CBC001`, `BLOOD02`)
   - **Test Name:** Full test name (e.g., `Complete Blood Count`)
   - **Category:** Select from dropdown:
     - Blood Test
     - Urine Test
     - Stool Test
     - Imaging
     - Biochemistry
     - Microbiology
     - Pathology
     - Other
   - **Description:** Optional details about the test

   **Pricing:**
   - **Price:** Enter amount in Taka (e.g., `500`)

   **Sample Requirements:**
   - **Sample Type:** e.g., "Blood", "Urine", "Saliva"
   - **Sample Volume:** e.g., "5ml", "10ml" (optional)
   - **Preparation Instructions:** e.g., "Fasting required" (optional)

   **Processing:**
   - **Turnaround Time:** e.g., "24 hours", "Same day", "48 hours"
   - **Is Active:** ✓ Check to make test available

5. **Click "Save"**

### Example Lab Test Entry:

```
Test Code: LIPID01
Test Name: Lipid Profile
Category: Blood Test
Description: Measures cholesterol and triglyceride levels
Price: 800
Sample Type: Blood
Sample Volume: 5ml
Preparation Instructions: 12 hours fasting required
Turnaround Time: 24 hours
Is Active: ✓ (checked)
```

---

## 2️⃣ How to Add/Edit Doctor Details

### Step-by-Step:

1. **Login to Admin Panel**
   - Go to http://localhost:8000/admin/

2. **Navigate to Users**
   ```
   Dashboard → ACCOUNTS section → Users
   ```

3. **Find the Doctor**
   - Use search box to find doctor by name/username
   - OR filter by "Role: Doctor"
   - Click on the doctor's name

4. **Scroll to "Additional Info" Section**
   
   Fill in these fields:
   - **Role:** Make sure "DOCTOR" is selected
   - **Phone:** Doctor's phone number
   - **Address:** Doctor's address
   - **Specialization:** 🔴 IMPORTANT - This shows on prescriptions
     - Examples:
       - `প্রসূতি ও গাইনী বিশেষজ্ঞ` (Gynecologist)
       - `মেডিসিন বিশেষজ্ঞ` (Medicine Specialist)
       - `সার্জন` (Surgeon)
       - `ক্যান্সার বিশেষজ্ঞ` (Cancer Specialist)
       - `শিশু রোগ বিশেষজ্ঞ` (Pediatrician)
       - `হৃদরোগ বিশেষজ্ঞ` (Cardiologist)
   - **License Number:** Doctor's medical license (e.g., `DOC-001`)
   - **Profile Picture:** Optional photo upload

5. **Click "Save"**

### Example Doctor Details:

```
Username: dr_rahman
First Name: আব্দুর
Last Name: রহমান
Role: DOCTOR
Phone: 01712345678
Specialization: মেডিসিন, ডায়াবেটিস ও হরমোন রোগ বিশেষজ্ঞ
License Number: DOC-005
```

---

## 3️⃣ How Doctor Details Show on Prescriptions

### Automatically Displayed:

When a doctor creates a prescription, these details show:

**On Prescription Header:**
```
┌─────────────────────────────────────┐
│ ইউনিভার্সাল হেলথ সার্ভিসেস         │
│                                     │
│        Dr. [Doctor's Full Name]     │
│        [Specialization]             │ ← From User.specialization
└─────────────────────────────────────┘
```

**On Prescription Footer:**
```
─────────────────────────
  [Doctor's Full Name]
  [Specialization]        ← From User.specialization
```

### If Specialization is Empty:
- Prescription will show: `MBBS` (default)
- **Fix:** Add specialization in admin as shown above

---

## 4️⃣ Current System Status

### ✅ Lab Tests (4 active tests)
1. **CBC001** - Complete Blood Count (CBC) - ৳500
2. **BLOOD01** - Blood Glucose (Fasting) - ৳150
3. **URINE01** - Urine Routine Examination - ৳200
4. **XRAY01** - Chest X-Ray - ৳800

### ✅ Doctors (8 active doctors)
All doctors have specializations set:
- ডাঃ আয়েশা ছিদ্দিকা - প্রসূতি ও গাইনী বিশেষজ্ঞ ✓
- ডাঃ খালিদ হোসেন - সার্জন ✓
- ডাঃ খাজা মোহাম্মদ - মেডিসিন বিশেষজ্ঞ ✓
- ডাঃ শাকেরা সুলতানা - ক্যান্সার বিশেষজ্ঞ ✓
- And 4 more...

### ✅ Prescriptions Working
All recent prescriptions show doctor names and specializations correctly.

---

## 5️⃣ Quick Reference: Common Lab Tests

### Blood Tests
```
Test Code: CBC001
Test Name: Complete Blood Count
Category: Blood Test
Price: 500
Sample: Blood (5ml)
Time: 24 hours

Test Code: BLOOD02
Test Name: Blood Sugar (Random)
Category: Blood Test
Price: 100
Sample: Blood (2ml)
Time: 2 hours

Test Code: LIPID01
Test Name: Lipid Profile
Category: Biochemistry
Price: 800
Sample: Blood (5ml), Fasting required
Time: 24 hours

Test Code: LIVER01
Test Name: Liver Function Test (LFT)
Category: Biochemistry
Price: 1200
Sample: Blood (5ml)
Time: 24 hours
```

### Urine Tests
```
Test Code: URINE01
Test Name: Urine Routine Examination
Category: Urine Test
Price: 200
Sample: Urine (50ml)
Time: 2 hours

Test Code: URINE02
Test Name: Urine Culture
Category: Microbiology
Price: 500
Sample: Urine (50ml, sterile container)
Time: 48 hours
```

### Imaging Tests
```
Test Code: XRAY01
Test Name: Chest X-Ray
Category: Imaging
Price: 800
Sample: N/A
Time: Same day

Test Code: XRAY02
Test Name: Abdominal X-Ray
Category: Imaging
Price: 1000
Sample: N/A
Time: Same day

Test Code: ULTRA01
Test Name: Ultrasound (Abdomen)
Category: Imaging
Price: 1500
Sample: N/A, Fasting required
Time: Same day
```

---

## 6️⃣ Managing Lab Tests

### Edit Existing Test:
1. Admin → Lab → Lab tests
2. Click on test name
3. Edit fields
4. Click "Save"

### Quick Edit Price:
1. Admin → Lab → Lab tests
2. Change price directly in list view
3. Prices are editable inline!

### Deactivate Test (Don't Delete):
1. Admin → Lab → Lab tests
2. Click on test
3. Uncheck "Is Active"
4. Click "Save"
- Test will not show for new orders but keeps history

### Bulk Actions:
- Select multiple tests (checkboxes)
- Choose action from dropdown:
  - Delete selected lab tests
  - Make selected tests active/inactive
- Click "Go"

---

## 7️⃣ Troubleshooting

### Problem: "Doctor name not showing on prescription"
**Solution:**
1. Check doctor has first_name and last_name filled
2. Go to Admin → Users → [Doctor]
3. Fill "First name" and "Last name" fields
4. Save

### Problem: "Specialization shows as MBBS instead of actual specialty"
**Solution:**
1. Go to Admin → Users → [Doctor]
2. Scroll to "Additional Info"
3. Fill "Specialization" field (can be in Bengali)
4. Save
5. Prescription will now show correct specialization

### Problem: "Can't add lab test - error"
**Solution:**
1. Make sure "Test Code" is unique (not used before)
2. Fill all required fields (marked with *)
3. Price must be a number
4. Check "Is Active" checkbox
5. Try again

### Problem: "Lab test not showing in doctor's order form"
**Solution:**
1. Check test is marked as "Is Active" ✓
2. Admin → Lab → Lab tests
3. Find the test
4. Check "Is active" checkbox
5. Save

---

## 8️⃣ Best Practices

### Lab Test Codes:
- Use consistent format: `CATEGORY + NUMBER`
- Examples: `CBC001`, `BLOOD02`, `XRAY01`, `LIVER01`
- Makes searching easier

### Pricing:
- Check prices regularly
- Update in bulk if needed
- Keep competitive with other centers

### Specializations:
- Use Bengali for local audience
- Be specific (e.g., "শিশু ও নবজাতক বিশেষজ্ঞ" not just "শিশু রোগ")
- Add multiple specialties if doctor has them

### Test Names:
- Use full medical names
- Add common abbreviations in description
- Example: Test Name: "Complete Blood Count", Description: "CBC - measures RBC, WBC, platelets"

---

## 9️⃣ Admin Quick Links

| Task | Path |
|------|------|
| Add Lab Test | Admin → Lab → Lab tests → Add |
| Edit Doctor | Admin → Accounts → Users → [Doctor Name] |
| View Orders | Admin → Lab → Lab orders |
| Manage Users | Admin → Accounts → Users |
| Check Appointments | Admin → Appointments → Appointments |

---

## 🎊 Summary

✅ **Lab Test Management:** Fully functional - admin can add/edit test names and prices  
✅ **Doctor Details:** Fully functional - admin can add/edit doctor specializations  
✅ **Prescription Display:** Working correctly - doctor names and specializations showing  
✅ **Current Data:** 4 lab tests, 8 doctors with specializations, all prescriptions working  

**Admin panel is ready to use!** 🚀

---

## 📞 Need More Help?

- Test the features by logging into admin panel
- Try adding a sample lab test
- Try editing a doctor's specialization
- Print a prescription to see the doctor details

All features are working correctly! 🎉

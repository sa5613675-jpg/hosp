# PRODUCTION DEPLOYMENT GUIDE
## Universal Health Services And Diagnostic Center

## ✓ SYSTEM READY FOR PRODUCTION

### Files to Run:
1. **prepare_production.py** - Cleans all fake data (ALREADY RUN)
2. **deploy_production_vps.sh** - Deploys to Ubuntu VPS

### Data Cleaned:
✓ 25 fake appointments deleted
✓ 15 fake patients deleted  
✓ All lab bills/orders cleared
✓ 90 real lab tests added
✓ All medicine stock reset to 0
✓ All financial records cleared
✓ All 16 user accounts preserved

### To Deploy on VPS:
```bash
# On your Ubuntu VPS
wget https://raw.githubusercontent.com/mahindx0-crypto/hosp/main/deploy_production_vps.sh
chmod +x deploy_production_vps.sh
sudo ./deploy_production_vps.sh
```

Then update:
- diagcenter/settings.py (DEBUG=False, ALLOWED_HOSTS, SECRET_KEY, Database)
- /etc/nginx/sites-available/diagcenter (your domain)
- Run: `python manage.py migrate && python manage.py collectstatic`

See full deployment documentation in the script comments.

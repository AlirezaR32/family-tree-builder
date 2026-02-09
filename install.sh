#!/bin/bash

echo "🌳 نصب سیستم شجره‌نامه خانوادگی"
echo "================================="
echo ""

# رنگ‌ها
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# بررسی وجود Python
echo "🔍 بررسی Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 یافت نشد. لطفاً ابتدا Python 3 را نصب کنید.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python یافت شد${NC}"

# بررسی وجود Node.js
echo "🔍 بررسی Node.js..."
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js یافت نشد. لطفاً ابتدا Node.js را نصب کنید.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Node.js یافت شد${NC}"
echo ""

# نصب بک‌اند
echo -e "${BLUE}📦 نصب وابستگی‌های بک‌اند...${NC}"
cd backend
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ وابستگی‌های بک‌اند نصب شد${NC}"
else
    echo -e "${RED}❌ خطا در نصب وابستگی‌های بک‌اند${NC}"
    exit 1
fi
cd ..
echo ""

# نصب فرانت‌اند
echo -e "${BLUE}📦 نصب وابستگی‌های فرانت‌اند...${NC}"
cd frontend
npm install
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ وابستگی‌های فرانت‌اند نصب شد${NC}"
else
    echo -e "${RED}❌ خطا در نصب وابستگی‌های فرانت‌اند${NC}"
    exit 1
fi
cd ..
echo ""

echo -e "${GREEN}🎉 نصب با موفقیت انجام شد!${NC}"
echo ""
echo "برای اجرای پروژه:"
echo "  1. Terminal اول: cd backend && python app.py"
echo "  2. Terminal دوم: cd frontend && npm run dev"
echo ""
echo "سپس به آدرس http://localhost:3000 بروید"

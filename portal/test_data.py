import os
import datetime
from PIL import Image, ImageDraw, ImageFont
import io

# Test data for both summarizer and fraud detector
class TestDataGenerator:
    def __init__(self):
        self.output_dir = "test_documents"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def create_legitimate_documents(self):
        """Generate legitimate legal documents for summarizer testing"""
        
        # 1. Employment Contract
        employment_contract = """
EMPLOYMENT AGREEMENT

This Employment Agreement ("Agreement") is entered into on January 15, 2025, between TechCorp Solutions (Pty) Ltd, a company incorporated under the laws of South Africa ("Company"), and Sarah Johnson ("Employee").

WHEREAS, the Company desires to employ the Employee in the capacity of Senior Software Developer; and

WHEREAS, the Employee agrees to be employed by the Company under the terms and conditions set forth herein;

NOW, THEREFORE, in consideration of the mutual covenants contained herein, the parties agree as follows:

1. POSITION AND DUTIES
Employee shall serve as Senior Software Developer and shall perform such duties as may be assigned by the Company's management team. Employee agrees to devote their full professional time and attention to the Company's business.

2. COMPENSATION
The Company shall pay Employee a gross monthly salary of R45,000 (Forty-Five Thousand Rand), payable monthly in arrears. Employee shall be entitled to annual performance reviews which may result in salary adjustments.

3. BENEFITS
Employee shall be entitled to:
- 21 working days annual leave
- Medical aid contribution (80% employer, 20% employee)
- Provident fund contribution (Company contributes 10% of basic salary)
- Professional development allowance of R10,000 per annum

4. TERMINATION
Either party may terminate this agreement with 30 (thirty) days written notice. The Company may terminate immediately for just cause including misconduct, breach of confidentiality, or poor performance.

5. CONFIDENTIALITY
Employee acknowledges that they may have access to confidential information and agrees to maintain strict confidentiality during and after employment.

IN WITNESS WHEREOF, the parties have executed this Agreement on the date first written above.

Company: _________________ Employee: _________________
TechCorp Solutions (Pty) Ltd Sarah Johnson
Date: _________________ Date: _________________
"""

        # 2. Rental Agreement
        rental_agreement = """
RESIDENTIAL LEASE AGREEMENT

Property Address: 123 Oak Street, Sandton, Johannesburg, 2196
Lease Term: 12 months commencing February 1, 2025

PARTIES:
Landlord: Property Investments SA (Pty) Ltd
Registration Number: 2019/123456/07
Tenant: Michael Williams

TERMS AND CONDITIONS:

1. RENTAL AMOUNT
Monthly rental: R18,500 (Eighteen Thousand Five Hundred Rand)
Deposit: R37,000 (Two months rental)
Lease administration fee: R1,200

2. PAYMENT TERMS
Rental is payable monthly in advance on the 1st of each month. Late payment after the 7th incurs a penalty of R500 plus 2% per month interest.

3. UTILITIES
Tenant responsible for electricity, water, gas, and municipal rates. Internet and security are included in rental.

4. MAINTENANCE
Landlord responsible for structural repairs. Tenant responsible for general maintenance and garden upkeep not exceeding R2,000 per incident.

5. TERMINATION
Either party may terminate with 30 days written notice. Early termination by tenant forfeits deposit.

6. PETS AND SUBLETTING
No pets allowed. Subletting requires written consent from Landlord.

Signed this 25th day of January, 2025

Landlord: _________________ Tenant: _________________
Property Investments SA Michael Williams
"""

        # 3. Service Agreement
        service_agreement = """
PROFESSIONAL SERVICES AGREEMENT

Client: Johnson & Associates Law Firm
Service Provider: Digital Marketing Pro (Pty) Ltd
Agreement Date: January 20, 2025

SCOPE OF SERVICES:
Digital Marketing Pro agrees to provide the following services:
- Website development and maintenance
- Search engine optimization (SEO)
- Social media management
- Monthly analytics reporting

SERVICE PERIOD: 12 months from February 1, 2025 to January 31, 2026

COMPENSATION:
Monthly retainer: R12,000 excluding VAT
Payment terms: 30 days from invoice date
Additional services billed at R800 per hour

DELIVERABLES:
- New website launch within 60 days
- Weekly social media posts
- Monthly SEO reports
- Quarterly strategy reviews

INTELLECTUAL PROPERTY:
All work products remain property of Client upon full payment. Service Provider retains right to use general methodologies and non-confidential techniques.

TERMINATION:
Either party may terminate with 30 days notice. Client liable for work completed to termination date.

This agreement constitutes the entire understanding between the parties.

Client Representative: _________________ Service Provider: _________________
James Johnson, Managing Partner Mark Stevens, CEO
Date: _________________ Date: _________________
"""

        return {
            "employment_contract.txt": employment_contract,
            "rental_agreement.txt": rental_agreement,
            "service_agreement.txt": service_agreement
        }
    
    def create_fraudulent_documents(self):
        """Generate fraudulent documents for fraud detector testing"""
        
        # 1. Investment Scam Document
        investment_scam = """
GUARANTEED INVESTMENT OPPORTUNITY - ACT NOW!

Dear Valued Investor,

URGENT ACTION REQUIRED - LIMITED TIME OFFER EXPIRES TODAY!

We are pleased to offer you an EXCLUSIVE investment opportunity with GUARANTEED returns of 50% per month! This is a RISK-FREE investment that has helped thousands of people achieve financial freedom.

SPECIAL BENEFITS:
- NO RISK whatsoever - 100% guaranteed returns
- Minimum investment only $500
- Get rich quick with our proven system
- Wire transfer required within 24 hours
- Processing fee of $200 (refundable)
- Handling charges apply ($50)

You have been SPECIALLY SELECTED for this confidential opportunity. Our previous investors have seen returns of 300-500% in just 6 months!

URGENT: This offer expires at midnight today. You must act immediately to secure your position.

To proceed:
1. Wire transfer $500 + $250 processing fee to account below
2. Provide your banking details for return transfers
3. Send copy of ID and proof of address immediately

Bank Details:
Account Name: Investment Holdings International
Account Number: 1234567890
Bank: First National Bank
Reference: INV2025URGENT

Contact us immediately:
Email: quickprofit@tempmail.com
Email: investnow@fakebank.org
Email: guaranteed@profits.net
Phone: +27 11 123 4567
Phone: +1 555 000 1234
WhatsApp: +44 20 7946 0958

This is your FINAL NOTICE. Don't miss this once-in-a-lifetime opportunity!

Signed: John Smith, Investment Director (unsigned)
Date: 32/13/2025 (INVALID DATE)
Company: Global Investments Ltd (UNREGISTERED)
"""

        # 2. Fake Legal Notice
        fake_legal_notice = """
FINAL LEGAL NOTICE - IMMEDIATE ACTION REQUIRED

CASE NO: ZA/2025/FAKE/001
REF: URGENT-LEGAL-MATTER

Dear Sir/Madam,

You are hereby notified that your account has been SUSPENDED due to suspicious activity. Immediate verification required to avoid legal action.

URGENT DETAILS:
- Your inheritance of $2,500,000 is being held
- Processing fee of $5,000 required immediately
- Clearance certificate must be obtained today
- Wire transfer only - no other payment methods accepted
- Final notice - legal action commences tomorrow

This matter involves the estate of a deceased relative who named you as beneficiary. However, due to new banking regulations, advance fees are required.

REQUIRED ACTIONS:
1. Verify immediately by calling +27 11 999 8888
2. Provide banking details and ID copy
3. Wire handling charges to: Account 9876543210
4. Obtain tax clearance certificate ($1,200)

WARNING: Failure to respond within 24 hours will result in:
- Forfeiture of inheritance
- Legal proceedings
- Criminal charges for non-compliance
- Asset seizure

This document has been backdated and amended without authorization to comply with regulations.

Contact Details:
lawyer@fakelaw.co.za
urgent@inheritancelaw.org
legal@fastmoney.net
Phone: +27 11 999 8888 (Always busy)
Phone: +1 800 SCAMMER

Signed: Dr. Fake Lawyer (FORGED SIGNATURE)
Johannesburg High Court (FALSIFIED LETTERHEAD)
Date: 2025/15/45 (IMPOSSIBLE DATE)
"""

        # 3. Cryptocurrency Scam
        crypto_scam = """
BITCOIN INVESTMENT CONTRACT - GUARANTEED PROFITS

EMERGENCY INVESTMENT ALERT - ACT FAST!

Dear Future Millionaire,

Congratulations! You have won our lottery selection for exclusive Bitcoin investment opportunity!

AMAZING BENEFITS:
- Guaranteed 200% return in 30 days - NO RISK!
- Minimum investment: Only $1,000
- Maximum investment: Unlimited (recommended $50,000+)
- Easy money - no experience needed
- Get rich quick with cryptocurrency boom

OUR PROVEN TRACK RECORD:
- 10,000+ satisfied investors
- Average return: 400% in 6 months
- Risk-free guarantee (money back if not satisfied)
- Confidential offshore accounts for tax benefits

URGENT: Bitcoin prices rising fast! This offer expires in 6 hours!

IMMEDIATE REQUIREMENTS:
1. Wire transfer funds within 2 hours
2. $500 handling fee (non-refundable)
3. $200 clearance certificate
4. Provide full banking details and passwords
5. Send scan of driver's license and passport

MULTIPLE CONTACT OPTIONS:
crypto@quickmoney.com
bitcoin@profits247.net
invest@guaranteed.biz
emergency@cryptoscam.org

Phone: +27 82 999 7777
Phone: +1 555 GET RICH
Phone: +44 77 7777 7777
WhatsApp: +234 802 123 4567

Transfer Details:
Bank: Bitcoin Bank International (FAKE BANK)
Account: CRYPTO123456789
Swift: BTCSCAM01

This contract has been altered and tampered with multiple times.

Manager: Tony Fake (Position fabricated)
Bitcoin Investment Corp (Company does not exist)
License: BTC001 (Counterfeit license)

Date: 2025/02/30 (Invalid date - February has no 30th)
Signature: [UNSIGNED DOCUMENT]
"""

        # 4. Fake Court Order
        fake_court_order = """
URGENT COURT ORDER - FINAL NOTICE

HIGH COURT OF SOUTH AFRICA
CASE NO: 12345/2025/FAKE

THE STATE vs. [YOUR NAME]

WHEREAS you have failed to appear for jury duty;
WHEREAS a warrant has been issued for your arrest;
WHEREAS immediate action is required to avoid imprisonment;

YOU ARE HEREBY ORDERED to contact this court immediately or face the following consequences:
- Immediate arrest warrant execution
- Asset seizure and forfeiture
- Criminal record notation
- R50,000 fine plus court costs

TO AVOID ARREST, you must:
1. Call immediately: +27 11 FAKE LAW (24 hours only)
2. Pay administrative fine of R5,000 via wire transfer
3. Provide personal details for verification
4. Purchase court clearance vouchers (R2,000)

PAYMENT DETAILS:
Account: Court Fees Collection (FABRICATED)
Bank: Legal Services Bank (DOES NOT EXIST)
Reference: URGENT_COURT_2025

This is your FINAL WARNING. Failure to comply within 4 hours will result in immediate arrest.

FORGED SIGNATURE: Judge Sarah Fake
FALSIFIED SEAL: Johannesburg High Court
Date: Today (No specific date - RED FLAG)

Contact: courtorder@fraud.co.za
Emergency: +27 82 SCAMMER

Document has been copied and altered multiple times.
"""

        return {
            "investment_scam.txt": investment_scam,
            "fake_legal_notice.txt": fake_legal_notice,
            "crypto_scam.txt": crypto_scam,
            "fake_court_order.txt": fake_court_order
        }
    
    def create_mixed_documents(self):
        """Generate borderline/mixed documents for edge case testing"""
        
        # 1. Legitimate but Poorly Written Contract
        poor_contract = """
AGREEMENT FOR SERVICES

This agreement is between John's Plumbing and Mary Smith for plumbing work.

Work to be done:
- Fix kitchen sink
- Replace bathroom tap
- Check for leaks

Cost: R2500
Payment: Cash only
When: Next week sometime

If there are problems, we will try to fix them. No guarantees though.

Both parties agree to this.

Signed: John (no last name)
Date: Some time in January
Phone: 082 123 4567
"""

        # 2. Aggressive but Legitimate Marketing
        aggressive_marketing = """
LIMITED TIME LEGAL SERVICES PROMOTION

Williams & Associates Attorneys

URGENT: Legal consultation prices increasing 300% next month!

Current special offer:
- First consultation: R500 (normally R1,500)
- Contract review: R2,000 (normally R5,000)
- Act now - offer expires January 31, 2025

Our proven track record:
- 95% success rate in contract disputes
- 20 years experience
- Admitted attorneys with proper credentials

This is a legitimate law firm registered with the Law Society of South Africa.
Registration: LSA/2005/12345

Contact:
info@williamslaw.co.za
Tel: +27 11 555 0123
Address: 456 Legal Street, Sandton, 2196

Terms: Standard legal fees apply. No guarantees on case outcomes.
Payment plans available. All consultations confidential.

Managing Partner: David Williams
Admitted Attorney, LLB (Wits), LLM (UCT)
"""

        return {
            "poor_contract.txt": poor_contract,
            "aggressive_marketing.txt": aggressive_marketing
        }
    
    def create_test_images(self):
        """Generate test images with text for OCR testing"""
        
        def create_document_image(text, filename, suspicious=False):
            # Create image
            img = Image.new('RGB', (800, 1000), color='white')
            draw = ImageDraw.Draw(img)
            
            # Try to use a basic font, fallback to default
            try:
                font = ImageFont.truetype("arial.ttf", 16)
                title_font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()
                title_font = ImageFont.load_default()
            
            # Add header
            if suspicious:
                draw.rectangle([(50, 50), (750, 100)], fill='red', outline='black')
                draw.text((60, 65), "URGENT - IMMEDIATE ACTION REQUIRED", fill='white', font=title_font)
            else:
                draw.rectangle([(50, 50), (750, 100)], fill='navy', outline='black')
                draw.text((60, 65), "LEGAL DOCUMENT", fill='white', font=title_font)
            
            # Add main text
            y_position = 120
            lines = text.split('\n')
            for line in lines[:25]:  # Limit lines to fit image
                if line.strip():
                    draw.text((60, y_position), line[:80], fill='black', font=font)
                    y_position += 25
            
            # Save image
            img_path = os.path.join(self.output_dir, filename)
            img.save(img_path)
            return img_path
        
        # Create images for different document types
        images = {}
        
        # Legitimate contract image
        contract_text = """RENTAL AGREEMENT
Property: 789 Main Road, Cape Town
Tenant: Alice Brown
Landlord: Cape Properties Ltd
Monthly Rent: R15,000
Lease Period: 12 months from March 1, 2025
Deposit: R30,000 (refundable)
Utilities: Tenant responsibility
Pets: One small pet allowed with deposit
Termination: 30 days written notice required
Signed: February 1, 2025"""
        
        images['legitimate_contract.png'] = create_document_image(contract_text, 'legitimate_contract.png', False)
        
        # Suspicious document image
        scam_text = """URGENT LEGAL NOTICE!!!
YOU HAVE WON $50,000!!!
IMMEDIATE ACTION REQUIRED
Wire transfer processing fee: $500
GUARANTEED RETURN ON INVESTMENT
NO RISK - 100% PROFIT ASSURED
Contact immediately: scam@fraud.com
Phone: +1 555 SCAMMER
This offer expires TODAY ONLY!
Send personal details NOW!
Account: 123FAKE456
Bank: International Money Bank"""
        
        images['suspicious_document.png'] = create_document_image(scam_text, 'suspicious_document.png', True)
        
        return images

    def save_test_data(self):
        """Save all test data to files"""
        
        print("Generating test data for Legal Document Tools...")
        
        # Create legitimate documents
        legitimate_docs = self.create_legitimate_documents()
        for filename, content in legitimate_docs.items():
            with open(os.path.join(self.output_dir, filename), 'w', encoding='utf-8') as f:
                f.write(content)
        
        # Create fraudulent documents
        fraudulent_docs = self.create_fraudulent_documents()
        for filename, content in fraudulent_docs.items():
            with open(os.path.join(self.output_dir, filename), 'w', encoding='utf-8') as f:
                f.write(content)
        
        # Create mixed documents
        mixed_docs = self.create_mixed_documents()
        for filename, content in mixed_docs.items():
            with open(os.path.join(self.output_dir, filename), 'w', encoding='utf-8') as f:
                f.write(content)
        
        # Create test images
        test_images = self.create_test_images()
        
        return {
            'legitimate': legitimate_docs,
            'fraudulent': fraudulent_docs,
            'mixed': mixed_docs,
            'images': test_images
        }

    def create_test_scenarios(self):
        """Create test scenarios with expected results"""
        
        scenarios = {
            "LEGITIMATE DOCUMENTS (Low Risk - Should Pass)": [
                {
                    "file": "employment_contract.txt",
                    "expected_risk": "LOW",
                    "expected_score": "< 30",
                    "key_features": "Proper legal structure, realistic terms, valid dates"
                },
                {
                    "file": "rental_agreement.txt", 
                    "expected_risk": "LOW",
                    "expected_score": "< 20",
                    "key_features": "Standard rental terms, proper formatting"
                },
                {
                    "file": "service_agreement.txt",
                    "expected_risk": "LOW", 
                    "expected_score": "< 25",
                    "key_features": "Professional service contract, clear terms"
                }
            ],
            
            "FRAUDULENT DOCUMENTS (High Risk - Should Fail)": [
                {
                    "file": "investment_scam.txt",
                    "expected_risk": "HIGH",
                    "expected_score": "> 80",
                    "key_features": "Guaranteed returns, urgency, multiple contacts"
                },
                {
                    "file": "fake_legal_notice.txt",
                    "expected_risk": "HIGH", 
                    "expected_score": "> 90",
                    "key_features": "Inheritance scam, advance fees, fake authority"
                },
                {
                    "file": "crypto_scam.txt",
                    "expected_risk": "HIGH",
                    "expected_score": "> 85",
                    "key_features": "Unrealistic promises, pressure tactics, fake credentials"
                },
                {
                    "file": "fake_court_order.txt",
                    "expected_risk": "HIGH",
                    "expected_score": "> 95",
                    "key_features": "Impersonating court, threats, payment demands"
                }
            ],
            
            "BORDERLINE DOCUMENTS (Medium Risk - Manual Review)": [
                {
                    "file": "poor_contract.txt",
                    "expected_risk": "MEDIUM",
                    "expected_score": "30-60",
                    "key_features": "Poor structure, vague terms, informal language"
                },
                {
                    "file": "aggressive_marketing.txt",
                    "expected_risk": "MEDIUM",
                    "expected_score": "25-45", 
                    "key_features": "Aggressive tactics but legitimate business"
                }
            ]
        }
        
        return scenarios

# Usage example and test runner
def run_test_generation():
    """Generate all test data and provide usage instructions"""
    
    generator = TestDataGenerator()
    
    print("🔧 LEGAL DOCUMENT TOOLS - TEST DATA GENERATOR")
    print("=" * 50)
    
    # Generate test data
    test_data = generator.save_test_data()
    scenarios = generator.create_test_scenarios()
    
    print(f"✅ Generated {len(test_data['legitimate'])} legitimate documents")
    print(f"✅ Generated {len(test_data['fraudulent'])} fraudulent documents") 
    print(f"✅ Generated {len(test_data['mixed'])} mixed documents")
    print(f"✅ Generated {len(test_data['images'])} test images")
    
    print(f"\n📁 All files saved to: {generator.output_dir}/")
    
    print("\n🧪 TEST SCENARIOS:")
    print("=" * 30)
    
    for category, tests in scenarios.items():
        print(f"\n{category}:")
        for test in tests:
            print(f"  📄 {test['file']}")
            print(f"     Expected Risk: {test['expected_risk']}")
            print(f"     Expected Score: {test['expected_score']}")
            print(f"     Features: {test['key_features']}")
    
    print("\n🚀 HOW TO TEST:")
    print("=" * 20)
    print("1. Run your Streamlit apps:")
    print("   streamlit run legal_summarizer.py")
    print("   streamlit run fraud_detector.py")
    print("")
    print("2. Upload test files from 'test_documents' folder")
    print("3. Compare actual results with expected outcomes")
    print("4. Fine-tune detection rules based on results")
    
    print("\n📊 EXPECTED RESULTS:")
    print("- Legitimate docs: Risk score 0-30 (LOW)")
    print("- Fraudulent docs: Risk score 70-100 (HIGH)")
    print("- Borderline docs: Risk score 30-70 (MEDIUM)")
    
    return test_data, scenarios

if __name__ == "__main__":
    # Generate test data
    test_data, scenarios = run_test_generation()
    
    print("\n✨ Test data generation complete!")
    print("You can now test both your summarizer and fraud detector with realistic documents.")
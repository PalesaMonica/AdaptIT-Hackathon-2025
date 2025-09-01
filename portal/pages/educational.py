import streamlit as st
import datetime
from gtts import gTTS
import tempfile
import os

# ---------------- Education Content Database ----------------
class LegalEducationContent:
    def __init__(self):
        self.topics = {
            "contracts": {
                "title": "Contract Law Basics",
                "description": "Understanding legal contracts and agreements",
                "content": self._get_contract_content(),
                "quiz": self._get_contract_quiz(),
                "difficulty": "Beginner"
            },
            "wills": {
                "title": "Wills and Estates",
                "description": "Everything about wills, estates, and inheritance",
                "content": self._get_wills_content(),
                "quiz": self._get_wills_quiz(),
                "difficulty": "Beginner"
            },
            "fraud": {
                "title": "Legal Fraud Prevention",
                "description": "Identifying and avoiding legal scams",
                "content": self._get_fraud_content(),
                "quiz": self._get_fraud_quiz(),
                "difficulty": "Intermediate"
            },
            "rights": {
                "title": "Your Legal Rights",
                "description": "Understanding your rights in South Africa",
                "content": self._get_rights_content(),
                "quiz": self._get_rights_quiz(),
                "difficulty": "Beginner"
            },
            "family_law": {
                "title": "Family Law",
                "description": "Marriage, divorce, and family legal matters",
                "content": self._get_family_law_content(),
                "quiz": self._get_family_law_quiz(),
                "difficulty": "Intermediate"
            },
            "labor": {
                "title": "Labor Law",
                "description": "Employment rights and workplace law",
                "content": self._get_labor_content(),
                "quiz": self._get_labor_quiz(),
                "difficulty": "Intermediate"
            }
        }
    
    def _get_contract_content(self):
        return {
            "overview": """
## What is a Contract?

A contract is a legally binding agreement between two or more parties. For a contract to be valid in South Africa, it must have:

### Essential Elements:
1. **Offer and Acceptance** - One party makes an offer, another accepts it
2. **Consideration** - Something of value exchanged (money, services, goods)
3. **Legal Capacity** - Parties must be legally able to enter contracts
4. **Legal Purpose** - The contract must be for something legal
5. **Certainty** - Terms must be clear and specific

### Common Contract Types:
- **Employment contracts** - Between employer and employee
- **Rental agreements** - Between landlord and tenant
- **Sales agreements** - For buying/selling goods or property
- **Service contracts** - For professional services
- **Insurance policies** - Protection against risks

### Your Rights in Contracts:
- Right to receive what was promised
- Right to cancel in certain circumstances (cooling-off periods)
- Right to claim damages if the other party breaches
- Right to have contracts in a language you understand

### Red Flags to Watch For:
- Pressure to sign immediately
- Terms that seem too good to be true
- Missing essential information
- Unclear or confusing language
- No cooling-off period for major purchases
            """,
            "practical_tips": """
## Practical Contract Tips

### Before Signing:
1. **Read everything** - Don't skip the fine print
2. **Ask questions** - Get explanations for unclear terms
3. **Check credentials** - Verify the other party is legitimate
4. **Get copies** - Always keep signed copies
5. **Consider legal advice** - For important contracts

### During Performance:
- Keep records of payments and communications
- Report problems immediately
- Know your cancellation rights
- Document any changes in writing

### Common Mistakes:
- Signing without reading
- Not keeping copies
- Agreeing to verbal changes
- Missing deadline dates
- Not understanding penalties
            """,
            "case_studies": """
## Real-World Examples

### Case 1: Employment Contract
**Situation**: Sarah signed an employment contract without reading the restraint of trade clause.
**Problem**: When she wanted to change jobs, she discovered she couldn't work for competitors for 2 years.
**Lesson**: Always read and understand restrictive clauses before signing.

### Case 2: Cell Phone Contract
**Situation**: John signed a 24-month cell phone contract but wanted to cancel after 6 months.
**Problem**: Early cancellation fees were very high - not clearly explained.
**Lesson**: Understand cancellation terms and fees before committing to long contracts.

### Case 3: Home Rental
**Situation**: Mary rented a flat but the lease didn't specify who pays for repairs.
**Problem**: Disputes arose about runtenance responsibilities.
**Lesson**: Ensure all terms are clearly written, not left to assumptions.
            """
        }
    
    def _get_wills_content(self):
        return {
            "overview": """
## Why You Need a Will

A will is a legal document that specifies how your assets should be distributed after your death. In South Africa, if you die without a will (intestate), the Intestate Succession Act determines how your estate is divided.

### Benefits of Having a Will:
1. **Control** - You decide who gets what
2. **Protection** - Ensures your wishes are followed
3. **Speed** - Faster estate administration
4. **Cost** - Reduces legal costs and disputes
5. **Care** - Choose guardians for minor children

### What Happens Without a Will:
- Government decides how assets are divided
- Spouse gets first R250,000 + 1/2 of rerunder
- Children share the rest equally
- Unmarried partners get nothing
- Process takes longer and costs more
- No choice in who manages your estate

### Will Requirements in South Africa:
- Must be 16+ years old
- Must be of sound mind
- Must be in writing
- Must be signed by you
- Must have 2+ witnesses (14+ years old)
- Witnesses cannot be beneficiaries
            """,
            "creating_wills": """
## Creating Your Will

### Step-by-Step Process:
1. **List your assets** - Property, bank accounts, investments, personal items
2. **Choose beneficiaries** - Who should inherit what
3. **Select an executor** - Someone to carry out your wishes
4. **Name guardians** - For minor children (if applicable)
5. **Write the will** - Clear, specific language
6. **Sign with witnesses** - Following legal requirements
7. **Store safely** - Keep original secure, tell executor location

### Types of Assets to Consider:
- **Real estate** - Houses, land, commercial property
- **Financial assets** - Bank accounts, investments, retirement funds
- **Personal property** - Vehicles, jewelry, furniture, art
- **Business interests** - Shares in companies, partnerships
- **Digital assets** - Online accounts, cryptocurrencies
- **Sentimental items** - Family heirlooms, photographs

### Updating Your Will:
Review and update when:
- You get married or divorced
- Children are born or adopted
- Major asset changes
- Beneficiaries die
- You move to another country
- Laws change significantly
            """,
            "estate_planning": """
## Beyond Basic Wills

### Advanced Estate Planning:
- **Trusts** - For tax benefits or protecting assets
- **Life insurance** - Providing for dependents
- **Business succession** - Continuing family businesses
- **Tax planning** - Minimizing estate taxes
- **International assets** - Cross-border considerations

### Common Estate Planning Mistakes:
1. **Procrastination** - Waiting too long to create a will
2. **DIY disasters** - Poorly written wills causing disputes
3. **Outdated documents** - Not updating after life changes
4. **Forgot assets** - Missing important properties or accounts
5. **Tax ignorance** - Not considering estate tax implications
6. **No communication** - Not telling family about plans

### Professional Help:
Consider consulting professionals for:
- Complex family situations
- Large estates
- Business assets
- International elements
- Tax optimization
- Trust structures
            """
        }
    
    def _get_fraud_content(self):
        return {
            "overview": """
## Legal Document Fraud: What You Need to Know

Document fraud is increasingly common in South Africa. Scammers create fake legal documents to steal money or personal information. Understanding the warning signs can protect you from becoming a victim.

### Common Types of Document Fraud:
1. **Fake inheritance notices** - Claims you've inherited money from unknown relatives
2. **Investment scams** - Documents promising unrealistic returns
3. **Fake legal threats** - Pretending to be from courts or law enforcement
4. **Property scams** - Forged deeds or fake rental agreements
5. **Employment fraud** - Fake job offers requiring upfront payments
6. **Insurance scams** - Bogus policies or fake claims

### How Fraudsters Operate:
- Use official-looking letterheads and seals
- Create urgent deadlines to pressure victims
- Request upfront fees for processing
- Ask for personal information like ID numbers
- Use complex legal language to confuse
- Impersonate legitimate authorities
            """,
            "warning_signs": """
## Red Flags to Watch For

### Document Red Flags:
- **Poor quality** - Spelling errors, bad formatting, unclear copies
- **Urgency pressure** - "Act now", "Limited time", "Final notice"
- **Upfront payments** - Fees required before receiving benefits
- **Too good to be true** - Unrealistic promises or offers
- **Missing information** - No proper contact details or registration numbers
- **Unofficial channels** - Communication only via email or WhatsApp

### Suspicious Contact Methods:
- Multiple email addresses from different doruns
- International phone numbers for local matters
- Requests to communicate only via messaging apps
- No physical address provided
- Refuses to meet in person
- Only accepts wire transfers or cash payments

### Language Red Flags:
- "Guaranteed" returns or outcomes
- "Risk-free" investments
- "Confidential" or "secret" opportunities  
- "You have been specially selected"
- "Processing fees" or "handling charges"
- "Clearance certificates" required
            """,
            "protection": """
## How to Protect Yourself

### Verification Steps:
1. **Check credentials** - Verify company registration numbers
2. **Research online** - Look up the company and individuals involved
3. **Contact authorities** - Check with relevant professional bodies
4. **Get second opinions** - Consult with trusted advisors
5. **Take time** - Don't rush important decisions
6. **Verify independently** - Contact organizations directly

### If You Suspect Fraud:
1. **Don't respond** - Don't provide personal information
2. **Don't pay** - Never send money for "processing fees"
3. **Keep records** - Save all communications as evidence
4. **Report it** - Contact police and relevant authorities
5. **Warn others** - Share information to protect others
6. **Get help** - Consult with legal professionals

### Reporting Fraud in South Africa:
- **SAPS** - South African Police Service
- **FSCA** - Financial Sector Conduct Authority  
- **Consumer Protection** - National Consumer Commission
- **Banking Ombudsman** - For banking-related fraud
- **Legal Practice Council** - For fake legal documents
            """
        }
    
    def _get_rights_content(self):
        return {
            "overview": """
## Your Constitutional Rights in South Africa

The South African Constitution guarantees fundamental rights to all citizens and residents. Understanding these rights empowers you to protect yourself and seek help when needed.

### Fundamental Rights Include:
1. **Equality** - Protection from unfair discrimination
2. **Human Dignity** - Right to be treated with respect
3. **Life** - Right to life and security of person
4. **Freedom and Security** - Protection from violence and detention
5. **Privacy** - Right to privacy in personal matters
6. **Freedom of Expression** - Right to speak and express opinions
7. **Assembly and Association** - Right to peaceful protest and join organizations
8. **Political Rights** - Right to vote and participate in politics
9. **Fair Labor Practices** - Rights at work
10. **Education** - Right to basic education

### Legal System Rights:
- **Right to legal representation** - You can have a lawyer
- **Right to rerun silent** - You don't have to incriminate yourself
- **Right to be informed** - You must be told why you're arrested
- **Right to fair trial** - Proper legal process must be followed
- **Right to interpreter** - Court proceedings in your language
            """,
            "practical_rights": """
## Rights in Daily Life

### Consumer Rights:
- Right to safe, quality goods and services
- Right to fair and honest dealing
- Right to choose suppliers freely
- Right to information in plain language
- Right to fair and reasonable prices
- Right to cancel certain contracts

### Housing Rights:
- Right to adequate housing
- Protection from illegal eviction
- Right to basic services (water, electricity)
- Fair rental practices
- Safe and healthy living conditions

### Healthcare Rights:
- Right to emergency medical treatment
- Right to informed consent
- Right to confidentiality
- Right to complain about poor service
- Right to access health records

### Education Rights:
- Right to basic education in official language of choice
- Right to equal educational opportunities
- Protection from discrimination in schools
- Right to safe learning environment
            """,
            "seeking_help": """
## Where to Get Help

### Legal Aid:
- **Legal Aid South Africa** - Free legal services for qualifying individuals
- **University law clinics** - Free or low-cost legal advice
- **Pro bono services** - Volunteer lawyers providing free services
- **Community advice offices** - Local legal assistance

### Human Rights Protection:
- **South African Human Rights Commission** - Constitutional rights violations
- **Commission for Gender Equality** - Gender-based discrimination
- **Public Protector** - Maladministration by government
- **Equality Court** - Unfair discrimination cases

### Ombudsman Services:
- **Banking Ombudsman** - Banking disputes
- **Insurance Ombudsman** - Insurance complaints  
- **Pension Funds Adjudicator** - Retirement fund issues
- **ICASA** - Telecommunications complaints

### When to Seek Legal Help:
- Arrested or charged with crime
- Facing eviction or housing problems
- Employment disputes or unfair dismissal
- Consumer complaints not resolved
- Discrimination or human rights violations
- Family law matters (divorce, runtenance)
            """
        }
    
    def _get_family_law_content(self):
        return {
            "overview": """
## Family Law in South Africa

Family law governs relationships between family members, including marriage, divorce, children's rights, and domestic violence. South African law recognizes various forms of marriage and provides protection for all family members.

### Types of Marriage:
1. **Civil Marriage** - Under Marriage Act (community of property default)
2. **Civil Union** - Same-sex or opposite-sex couples
3. **Customary Marriage** - Traditional African marriages
4. **Religious Marriages** - Must also be civil marriages to be legally recognized

### Marriage Property Regimes:
- **In Community of Property** - All assets and debts shared equally
- **Out of Community of Property** - Assets rerun separate
- **Accrual System** - Growth during marriage is shared

### Children's Rights:
- Right to know both parents
- Right to care and protection
- Right to basic nutrition, shelter, healthcare, education
- Protection from abuse and neglect
- Best interests principle in all decisions
            """,
            "divorce": """
## Divorce and Separation

### Grounds for Divorce:
1. **Irretrievable breakdown** - Marriage has broken down permanently
2. **Mental illness** - Spouse has been mentally ill for 2+ years
3. **Imprisonment** - Spouse imprisoned for 5+ years with 12+ months reruning

### Divorce Process:
1. **Attempt reconciliation** - Court may require counseling
2. **File papers** - Summons and particulars of claim
3. **Service** - Other spouse must be notified
4. **Response** - Spouse can defend or agree
5. **Settlement negotiations** - Try to agree on terms
6. **Court hearing** - If agreement not reached
7. **Decree** - Final divorce order

### Issues to Resolve:
- **runtenance** - Spousal and child support
- **Custody and access** - Care of children
- **Division of assets** - Property and investments
- **Pension benefits** - Retirement fund sharing
- **Household goods** - Personal property division

### Child Custody Options:
- **Sole custody** - One parent has primary responsibility
- **Joint custody** - Both parents share decisions
- **Shared residence** - Child lives with both parents
- **Contact arrangements** - Visitation schedules
            """,
            "domestic_violence": """
## Domestic Violence Protection

### What is Domestic Violence?
Physical, emotional, psychological, or economic abuse between people in domestic relationships, including:
- Current or former spouses
- Life partners
- Dating relationships
- Family members
- People sharing a home

### Types of Abuse:
- **Physical** - Hitting, pushing, restraining
- **Emotional** - Threats, intimidation, humiliation
- **Sexual** - Forced sexual acts, sexual harassment
- **Economic** - Controlling money, preventing work
- **Psychological** - Mind games, isolation from family/friends

### Protection Orders:
- **Interim Protection Order** - Immediate temporary protection
- **Final Protection Order** - Long-term protection after court hearing
- **Can include** - No contact, stay away from home/work, surrender weapons

### Getting Help:
1. **Call police** - 10111 for immediate danger
2. **Go to magistrate's court** - Apply for protection order
3. **Contact shelters** - Safe accommodation available
4. **Get medical help** - Document injuries
5. **Tell someone** - Friend, family, counselor

### Support Services:
- **Stop Gender Violence Helpline** - 0800 150 150
- **Childline** - 08000 55 555 (for children)
- **Crisis counseling** - Available through NGOs
- **Legal aid** - Free legal assistance available
            """
        }
    
    def _get_labor_content(self):
        return {
            "overview": """
## Employment Rights in South Africa

The Labour Relations Act and other employment laws protect workers' rights and establish fair workplace practices. Understanding these rights helps ensure fair treatment at work.

### Basic Employment Rights:
1. **Fair labor practices** - Protection from unfair treatment
2. **Collective bargaining** - Right to join unions and negotiate
3. **Safe working conditions** - Healthy and safe workplace
4. **Equal treatment** - No unfair discrimination
5. **Fair dismissal** - Proper procedures must be followed
6. **Reasonable working hours** - Limits on work time

### Types of Employment:
- **Permanent employees** - Full employment rights and benefits
- **Fixed-term contracts** - Limited duration employment
- **Casual workers** - Irregular work arrangements
- **Independent contractors** - Self-employed service providers

### Working Time Rights:
- **Maximum 45 hours per week** (or 9 hours per day)
- **Overtime pay** - 1.5x normal rate
- **Rest periods** - Daily and weekly rest
- **Annual leave** - 21 consecutive days per year
- **Sick leave** - 30 days over 3-year cycle
- **Maternity leave** - 4 months for mothers
            """,
            "dismissal": """
## Unfair Dismissal Protection

### Fair Reasons for Dismissal:
1. **Misconduct** - Breaking workplace rules or policies
2. **Incapacity** - Unable to perform job duties
3. **Operational requirements** - Retrenchment due to business needs

### Unfair Dismissal Includes:
- Dismissal without proper procedure
- Discrimination-based dismissal
- Dismissal for exercising rights
- Dismissal during pregnancy
- Dismissal for union membership

### Dismissal Procedures:
1. **Investigation** - Fair inquiry into allegations
2. **Hearing** - Chance to respond and present case
3. **Decision** - Based on evidence and circumstances
4. **Appeal** - Opportunity to challenge decision

### Remedies for Unfair Dismissal:
- **Reinstatement** - Getting your job back
- **Re-employment** - Similar position with same employer
- **Compensation** - Up to 12 months salary

### Where to Get Help:
- **CCMA** - Commission for Conciliation, Mediation and Arbitration
- **Labour Court** - For complex legal matters
- **Trade unions** - Member representation and advice
- **Legal Aid** - Free legal assistance if qualifying
            """,
            "workplace_rights": """
## Workplace Safety and Discrimination

### Health and Safety Rights:
- Right to safe working environment
- Right to safety training and equipment
- Right to report unsafe conditions
- Right to refuse dangerous work
- Right to workers' compensation for injuries

### Discrimination Protection:
Protected from unfair discrimination based on:
- Race, gender, age, disability
- Religion, culture, language
- Sexual orientation
- Pregnancy
- HIV status
- Political beliefs

### Sexual Harassment Protection:
- Right to work free from sexual harassment
- Employer must have policies and procedures
- Right to report incidents safely
- Protection from victimization

### Maternity Rights:
- No dismissal during pregnancy
- 4 months maternity leave
- Right to return to same or similar job
- Breastfeeding breaks for nursing mothers
- Protection from pregnancy discrimination

### Union Rights:
- Right to join trade union
- Right to participate in union activities
- Protection from victimization
- Right to collective bargaining
- Right to strike (with restrictions)

### Minimum Wage:
- National minimum wage applies to most workers
- Some sectors have higher sectoral determinations
- Regular increases to keep pace with inflation
- Enforcement through Department of Employment and Labour
            """
        }
    
    def _get_contract_quiz(self):
        return [
            {
                "question": "What are the essential elements of a valid contract?",
                "options": [
                    "Offer, acceptance, and signatures",
                    "Offer, acceptance, consideration, legal capacity, and legal purpose",
                    "Money, signatures, and witnesses",
                    "Written agreement and notarization"
                ],
                "correct": 1,
                "explanation": "A valid contract requires offer, acceptance, consideration (something of value exchanged), legal capacity (ability to contract), and legal purpose (lawful objective)."
            },
            {
                "question": "When should you be most cautious about signing a contract?",
                "options": [
                    "When there's pressure to sign immediately",
                    "When the terms seem too good to be true",
                    "When important information is missing",
                    "All of the above"
                ],
                "correct": 3,
                "explanation": "All these situations are red flags. Always take time to read, understand, and verify contract terms before signing."
            },
            {
                "question": "What should you always do before signing a contract?",
                "options": [
                    "Sign quickly to avoid losing the deal",
                    "Read only the run terms, skip fine print",
                    "Read everything and ask questions about unclear terms",
                    "Let someone else read it for you"
                ],
                "correct": 2,
                "explanation": "Always read the entire contract, including fine print, and ask for explanations of anything unclear before signing."
            }
        ]
    
    def _get_wills_quiz(self):
        return [
            {
                "question": "What happens if you die without a will in South Africa?",
                "options": [
                    "Your assets go to the government",
                    "The Intestate Succession Act determines how assets are divided",
                    "Your oldest child inherits everything",
                    "Your spouse gets everything automatically"
                ],
                "correct": 1,
                "explanation": "If you die without a will (intestate), the Intestate Succession Act determines how your estate is distributed, which may not align with your wishes."
            },
            {
                "question": "What is the minimum age to make a will in South Africa?",
                "options": ["18 years old", "21 years old", "16 years old", "14 years old"],
                "correct": 2,
                "explanation": "In South Africa, you can make a will from age 16, provided you are of sound mind."
            },
            {
                "question": "How many witnesses are required for a will in South Africa?",
                "options": ["1 witness", "2 witnesses", "3 witnesses", "No witnesses needed"],
                "correct": 1,
                "explanation": "South African law requires at least 2 witnesses who are at least 14 years old and are not beneficiaries in the will."
            }
        ]
    
    def _get_fraud_quiz(self):
        return [
            {
                "question": "What is a major red flag in investment documents?",
                "options": [
                    "Detailed risk disclosures",
                    "Contact information provided",
                    "Guaranteed returns with no risk",
                    "Professional letterhead"
                ],
                "correct": 2,
                "explanation": "Any investment promising 'guaranteed returns' with 'no risk' is almost certainly a scam. All legitimate investments carry some risk."
            },
            {
                "question": "What should you do if you receive a suspicious legal document?",
                "options": [
                    "Respond immediately to avoid penalties",
                    "Send the requested payment to be safe",
                    "Verify independently and don't respond hastily",
                    "Forward it to friends for their opinion"
                ],
                "correct": 2,
                "explanation": "Always verify suspicious documents independently through official channels. Never rush to respond or send money."
            },
            {
                "question": "Which is NOT a common fraud tactic?",
                "options": [
                    "Creating artificial urgency",
                    "Requesting upfront payments",
                    "Providing clear contact information and credentials",
                    "Making unrealistic promises"
                ],
                "correct": 2,
                "explanation": "Legitimate organizations provide clear contact information and proper credentials. Fraudsters often avoid this to prevent verification."
            }
        ]
    
    def _get_rights_quiz(self):
        return [
            {
                "question": "According to the South African Constitution, everyone has the right to:",
                "options": [
                    "Expensive healthcare only",
                    "Emergency medical treatment",
                    "Private education only",
                    "Unlimited freedom of expression"
                ],
                "correct": 1,
                "explanation": "The Constitution guarantees the right to emergency medical treatment for everyone, regardless of their ability to pay."
            },
            {
                "question": "If you cannot afford a lawyer, what options do you have?",
                "options": [
                    "Represent yourself only",
                    "Legal Aid South Africa and pro bono services",
                    "Borrow money for expensive lawyers",
                    "Give up on legal assistance"
                ],
                "correct": 1,
                "explanation": "Legal Aid South Africa provides free legal services to qualifying individuals, and many lawyers offer pro bono services."
            },
            {
                "question": "Where can you report human rights violations?",
                "options": [
                    "Only to the police",
                    "South African Human Rights Commission",
                    "Only to your employer",
                    "Nowhere - they can't be reported"
                ],
                "correct": 1,
                "explanation": "The South African Human Rights Commission investigates human rights violations and constitutional rights breaches."
            }
        ]
    
    def _get_family_law_quiz(self):
        return [
            {
                "question": "In South Africa, what is the default property regime for civil marriages?",
                "options": [
                    "Out of community of property",
                    "In community of property",
                    "Accrual system",
                    "Separate property"
                ],
                "correct": 1,
                "explanation": "Civil marriages in South Africa are automatically in community of property unless an antenuptial contract specifies otherwise."
            },
            {
                "question": "What type of protection can you get against domestic violence?",
                "options": [
                    "Only police protection",
                    "Protection orders from magistrate's court",
                    "Only family support",
                    "No legal protection available"
                ],
                "correct": 1,
                "explanation": "You can apply for protection orders at the magistrate's court, which can include no-contact orders and other protective measures."
            },
            {
                "question": "Which is a valid ground for divorce in South Africa?",
                "options": [
                    "Different religious beliefs",
                    "Irretrievable breakdown of marriage",
                    "Financial difficulties",
                    "In-law problems"
                ],
                "correct": 1,
                "explanation": "Irretrievable breakdown of marriage is the most common ground for divorce, meaning the marriage has permanently broken down."
            }
        ]
    
    def _get_labor_quiz(self):
        return [
            {
                "question": "What is the maximum number of hours you can work per week in South Africa?",
                "options": ["40 hours", "45 hours", "50 hours", "No limit"],
                "correct": 1,
                "explanation": "The Basic Conditions of Employment Act sets the maximum working week at 45 hours for most employees."
            },
            {
                "question": "If you are unfairly dismissed, where can you take your case?",
                "options": [
                    "Only to your union",
                    "CCMA (Commission for Conciliation, Mediation and Arbitration)",
                    "Only to the police",
                    "Nowhere - employers can dismiss anyone"
                ],
                "correct": 1,
                "explanation": "The CCMA deals with unfair dismissal cases and provides conciliation, mediation, and arbitration services."
            },
            {
                "question": "How much annual leave are you entitled to?",
                "options": [
                    "15 consecutive days",
                    "21 consecutive days",
                    "30 consecutive days",
                    "No guaranteed leave"
                ],
                "correct": 1,
                "explanation": "The Basic Conditions of Employment Act guarantees 21 consecutive days of annual leave for most employees."
            }
        ]

# ---------------- Progress Tracking ----------------
class ProgressTracker:
    def __init__(self):
        if 'progress' not in st.session_state:
            st.session_state.progress = {
                'completed_topics': [],
                'quiz_scores': {},
                'total_score': 0,
                'certificates': []
            }
    
    def mark_topic_complete(self, topic_key):
        if topic_key not in st.session_state.progress['completed_topics']:
            st.session_state.progress['completed_topics'].append(topic_key)
    
    def record_quiz_score(self, topic_key, score, total):
        st.session_state.progress['quiz_scores'][topic_key] = {
            'score': score,
            'total': total,
            'percentage': (score / total) * 100
        }
        self.update_total_score()
    
    def update_total_score(self):
        if st.session_state.progress['quiz_scores']:
            total_percentage = sum([quiz['percentage'] for quiz in st.session_state.progress['quiz_scores'].values()])
            st.session_state.progress['total_score'] = total_percentage / len(st.session_state.progress['quiz_scores'])
    
    def generate_certificate(self, topic_key, content):
        certificate = {
            'topic': topic_key,
            'title': content.topics[topic_key]['title'],
            'date': datetime.datetime.now().strftime("%Y-%m-%d"),
            'score': st.session_state.progress['quiz_scores'].get(topic_key, {}).get('percentage', 0)
        }
        if certificate not in st.session_state.progress['certificates']:
            st.session_state.progress['certificates'].append(certificate)
        return certificate

# ---------------- Audio Generation ----------------
def generate_audio(text, language='en'):
    """Generate audio from text using gTTS"""
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(tmp_file.name)
            return tmp_file.name
    except Exception as e:
        st.error(f"Error generating audio: {str(e)}")
        return None

# ---------------- run Application ----------------
def run():
    st.set_page_config(
        page_title="Legal Education for South Africa",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize content and progress tracker
    content = LegalEducationContent()
    progress = ProgressTracker()
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .run-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .topic-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #2a5298;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .progress-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
    }
    .quiz-question {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .correct-answer {
        background: #d4edda;
        color: #155724;
        padding: 0.5rem;
        border-radius: 4px;
        margin-top: 0.5rem;
    }
    .incorrect-answer {
        background: #f8d7da;
        color: #721c24;
        padding: 0.5rem;
        border-radius: 4px;
        margin-top: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="run-header">
        <h1>⚖️ Legal Education for South Africa</h1>
        <p>Empowering South Africans with Essential Legal Knowledge</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("🔍 Navigation")
    
    # run menu
    menu_options = [
        " Home",
        "Learn Topics",
        " Take Quiz",
        " Progress Dashboard",
        " Certificates",
        " Legal Resources"
    ]
    
    selected_menu = st.sidebar.selectbox("Choose an option:", menu_options)
    
    # Topic selection for learning and quizzes
    if selected_menu in ["Learn Topics", "Take Quiz"]:
        st.sidebar.subheader("Select Topic")
        topic_options = []
        for key, topic in content.topics.items():
            difficulty_emoji = "🟢" if topic['difficulty'] == 'Beginner' else "🟡"
            topic_options.append(f"{difficulty_emoji} {topic['title']}")
        
        selected_topic_display = st.sidebar.selectbox("Choose a topic:", topic_options)
        # Extract topic key from display name
        selected_topic_key = None
        for key, topic in content.topics.items():
            if topic['title'] in selected_topic_display:
                selected_topic_key = key
                break
    
    # run content area
    if selected_menu == "Home":
        show_home_page(content, progress)
    elif selected_menu == "Learn Topics":
        show_learning_page(content, progress, selected_topic_key)
    elif selected_menu == "Take Quiz":
        show_quiz_page(content, progress, selected_topic_key)
    elif selected_menu == " Progress Dashboard":
        show_progress_dashboard(progress, content)
    elif selected_menu == " Certificates":
        show_certificates_page(progress)
    elif selected_menu == " Legal Resources":
        show_resources_page()

def show_home_page(content, progress):
    """Display the home page with overview and quick access"""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Welcome to Legal Education")
        
        st.markdown("""
        ### Why Legal Education Matters
        
        Understanding your legal rights and responsibilities is crucial in today's world. This platform provides:
        
        ✅ **Practical Legal Knowledge** - Real-world information you can use  
        ✅ **South African Context** - Laws and procedures specific to SA  
        ✅ **Interactive Learning** - Quizzes and assessments to test understanding  
        ✅ **Progress Tracking** - Monitor your learning journey  
        ✅ **Audio Support** - Listen to content on the go  
        
        ### Available Topics
        """)
        
        # Display topic overview cards
        for key, topic in content.topics.items():
            difficulty_color = "#28a745" if topic['difficulty'] == 'Beginner' else "#ffc107"
            
            st.markdown(f"""
            <div class="topic-card">
                <h4>{topic['title']}</h4>
                <p>{topic['description']}</p>
                <span style="background: {difficulty_color}; color: white; padding: 0.2rem 0.5rem; border-radius: 12px; font-size: 0.8rem;">
                    {topic['difficulty']}
                </span>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.header(" Your Progress")
        
        # Progress overview
        completed_topics = len(st.session_state.progress['completed_topics'])
        total_topics = len(content.topics)
        completion_rate = (completed_topics / total_topics) * 100 if total_topics > 0 else 0
        
        st.metric("Topics Completed", f"{completed_topics}/{total_topics}")
        st.progress(completion_rate / 100)
        st.text(f"Overall Progress: {completion_rate:.1f}%")
        
        # Quick stats
        if st.session_state.progress['quiz_scores']:
            avg_score = st.session_state.progress['total_score']
            st.metric("Average Quiz Score", f"{avg_score:.1f}%")
            
            st.subheader("Recent Quiz Scores")
            for topic, score_data in st.session_state.progress['quiz_scores'].items():
                topic_title = content.topics[topic]['title']
                st.write(f"• {topic_title}: {score_data['score']}/{score_data['total']} ({score_data['percentage']:.1f}%)")

def show_learning_page(content, progress, topic_key):
    """Display learning content for a specific topic"""
    if not topic_key:
        st.warning("Please select a topic from the sidebar.")
        return
    
    topic = content.topics[topic_key]
    
    st.header(topic['title'])
    st.subheader(topic['description'])
    
    # Topic difficulty indicator
    difficulty_color = "#28a745" if topic['difficulty'] == 'Beginner' else "#ffc107"
    st.markdown(f"""
    <span style="background: {difficulty_color}; color: white; padding: 0.3rem 0.7rem; border-radius: 15px; font-size: 0.9rem;">
         {topic['difficulty']} Level
    </span>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Content sections
    topic_content = topic['content']
    
    # Create tabs for different content sections
    tab_names = list(topic_content.keys())
    tabs = st.tabs([name.replace('_', ' ').title() for name in tab_names])
    
    for i, (section_key, section_content) in enumerate(topic_content.items()):
        with tabs[i]:
            st.markdown(section_content)
            
            # Audio generation option
            if st.button(f"🔊 Listen to {section_key.replace('_', ' ').title()}", key=f"audio_{topic_key}_{section_key}"):
                with st.spinner("Generating audio..."):
                    # Clean text for TTS (remove markdown)
                    clean_text = section_content.replace('#', '').replace('*', '').replace('**', '')
                    audio_file = generate_audio(clean_text)
                    if audio_file:
                        audio_bytes = open(audio_file, 'rb').read()
                        st.audio(audio_bytes, format='audio/mp3')
                        # Clean up temp file
                        os.unlink(audio_file)
    
    # Mark topic as completed
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(" Mark Topic as Completed", key=f"complete_{topic_key}"):
            progress.mark_topic_complete(topic_key)
            st.success(f"Great job! You've completed {topic['title']}")
            st.balloons()

def show_quiz_page(content, progress, topic_key):
    """Display quiz for a specific topic"""
    if not topic_key:
        st.warning("Please select a topic from the sidebar.")
        return
    
    topic = content.topics[topic_key]
    quiz_questions = topic['quiz']
    
    st.header(f"Quiz: {topic['title']}")
    st.subheader("Test Your Knowledge")
    
    st.markdown(f"""
    **Instructions:**  
    - Read each question carefully  
    - Select the best answer  
    - Click 'Submit Quiz' when you're done  
    - You'll receive instant feedback on your answers  
    """)
    
    st.markdown("---")
    
    # Initialize session state for quiz answers
    if f'quiz_answers_{topic_key}' not in st.session_state:
        st.session_state[f'quiz_answers_{topic_key}'] = {}
    
    # Display questions
    for i, question in enumerate(quiz_questions):
        st.markdown(f"""
        <div class="quiz-question">
            <h4>Question {i+1}</h4>
            <p>{question['question']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Radio buttons for options
        answer = st.radio(
            "Select your answer:",
            question['options'],
            key=f"q_{topic_key}_{i}",
            index=None
        )
        
        if answer:
            st.session_state[f'quiz_answers_{topic_key}'][i] = question['options'].index(answer)
        
        st.markdown("---")
    
    # Submit quiz
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Submit Quiz", key=f"submit_quiz_{topic_key}"):
            # Check if all questions are answered
            if len(st.session_state[f'quiz_answers_{topic_key}']) != len(quiz_questions):
                st.error("Please answer all questions before submitting.")
                return
            
            # Calculate score
            correct_answers = 0
            results = []
            
            for i, question in enumerate(quiz_questions):
                user_answer = st.session_state[f'quiz_answers_{topic_key}'][i]
                is_correct = user_answer == question['correct']
                if is_correct:
                    correct_answers += 1
                
                results.append({
                    'question': question['question'],
                    'user_answer': question['options'][user_answer],
                    'correct_answer': question['options'][question['correct']],
                    'is_correct': is_correct,
                    'explanation': question['explanation']
                })
            
            # Record score
            progress.record_quiz_score(topic_key, correct_answers, len(quiz_questions))
            
            # Display results
            st.header(" Quiz Results")
            
            score_percentage = (correct_answers / len(quiz_questions)) * 100
            
            if score_percentage >= 80:
                st.success(f" Excellent! You scored {correct_answers}/{len(quiz_questions)} ({score_percentage:.1f}%)")
                st.balloons()
                # Generate certificate
                progress.generate_certificate(topic_key, content)
            elif score_percentage >= 60:
                st.warning(f" Good job! You scored {correct_answers}/{len(quiz_questions)} ({score_percentage:.1f}%)")
            else:
                st.error(f"Keep studying! You scored {correct_answers}/{len(quiz_questions)} ({score_percentage:.1f}%)")
            
            # Show detailed results
            st.subheader("Detailed Results")
            
            for i, result in enumerate(results):
                if result['is_correct']:
                    st.markdown(f"""
                    <div class="correct-answer">
                        <h5>Question {i+1}:  Correct</h5>
                        <p><strong>Q:</strong> {result['question']}</p>
                        <p><strong>Your answer:</strong> {result['user_answer']}</p>
                        <p><strong>Explanation:</strong> {result['explanation']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="incorrect-answer">
                        <h5>Question {i+1}:  Incorrect</h5>
                        <p><strong>Q:</strong> {result['question']}</p>
                        <p><strong>Your answer:</strong> {result['user_answer']}</p>
                        <p><strong>Correct answer:</strong> {result['correct_answer']}</p>
                        <p><strong>Explanation:</strong> {result['explanation']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Clear quiz answers for retake
            del st.session_state[f'quiz_answers_{topic_key}']

def show_progress_dashboard(progress, content):
    """Display progress dashboard"""
    st.header(" Your Learning Progress")
    
    # Overall statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        completed_topics = len(st.session_state.progress['completed_topics'])
        total_topics = len(content.topics)
        st.metric("Topics Completed", f"{completed_topics}/{total_topics}")
    
    with col2:
        quizzes_taken = len(st.session_state.progress['quiz_scores'])
        st.metric("Quizzes Taken", quizzes_taken)
    
    with col3:
        if st.session_state.progress['total_score']:
            avg_score = st.session_state.progress['total_score']
            st.metric("Average Score", f"{avg_score:.1f}%")
        else:
            st.metric("Average Score", "N/A")
    
    with col4:
        certificates = len(st.session_state.progress['certificates'])
        st.metric("Certificates Earned", certificates)
    
    st.markdown("---")
    
    # Progress by topic
    st.subheader(" Progress by Topic")
    
    for key, topic in content.topics.items():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"**{topic['title']}**")
            
            # Completion status
            is_completed = key in st.session_state.progress['completed_topics']
            completion_status = " Completed" if is_completed else " In Progress"
            
            # Quiz score
            quiz_info = "Not taken"
            if key in st.session_state.progress['quiz_scores']:
                score_data = st.session_state.progress['quiz_scores'][key]
                quiz_info = f"{score_data['score']}/{score_data['total']} ({score_data['percentage']:.1f}%)"
            
            st.write(f"Status: {completion_status} | Quiz: {quiz_info}")
        
        with col2:
            # Progress indicator
            progress_value = 0
            if is_completed:
                progress_value += 50
            if key in st.session_state.progress['quiz_scores']:
                progress_value += 50
            
            st.progress(progress_value / 100)
            st.write(f"{progress_value}%")

def show_certificates_page(progress):
    """Display earned certificates"""
    st.header(" Your Certificates")
    
    if not st.session_state.progress['certificates']:
        st.info("Complete quizzes with 80% or higher scores to earn certificates!")
        return
    
    st.write(f"You have earned **{len(st.session_state.progress['certificates'])}** certificates!")
    
    for cert in st.session_state.progress['certificates']:
        st.markdown(f"""
        <div style="border: 2px solid #gold; padding: 2rem; margin: 1rem 0; border-radius: 10px; background: linear-gradient(45deg, #f9f9f9, #ffffff); text-align: center;">
            <h2> Certificate of Completion</h2>
            <h3>{cert['title']}</h3>
            <p>This certifies that the learner has successfully completed the course</p>
            <p><strong>Score Achieved:</strong> {cert['score']:.1f}%</p>
            <p><strong>Date:</strong> {cert['date']}</p>
            <p><em>Legal Education Platform - South Africa</em></p>
        </div>
        """, unsafe_allow_html=True)

def show_resources_page():
    """Display legal resources and contacts"""
    st.header(" Legal Resources in South Africa")
    
    st.markdown("""
    ### Emergency Contacts
    - **Police Emergency:** 10111
    - **Stop Gender Violence:** 0800 150 150
    - **Childline:** 08000 55 555
    
    ### Legal Aid Organizations
    """)
    
    resources = [
        {
            "name": "Legal Aid South Africa",
            "description": "Free legal services for qualifying individuals",
            "contact": "0800 110 110",
            "website": "www.legal-aid.co.za"
        },
        {
            "name": "South African Human Rights Commission",
            "description": "Constitutional rights violations",
            "contact": "011 877 3600",
            "website": "www.sahrc.org.za"
        },
        {
            "name": "CCMA",
            "description": "Employment disputes and unfair dismissals",
            "contact": "086 1600 250",
            "website": "www.ccma.org.za"
        },
        {
            "name": "National Consumer Commission",
            "description": "Consumer complaints and protection",
            "contact": "012 428 7000",
            "website": "www.thencc.gov.za"
        },
        {
            "name": "Banking Ombudsman",
            "description": "Banking disputes and complaints",
            "contact": "011 712 1800",
            "website": "www.obssa.co.za"
        }
    ]
    
    for resource in resources:
        st.markdown(f"""
        <div class="topic-card">
            <h4>{resource['name']}</h4>
            <p>{resource['description']}</p>
            <p><strong>Contact:</strong> {resource['contact']}</p>
            <p><strong>Website:</strong> {resource['website']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    ### Important Notes
    - This platform provides educational information only
    - For specific legal advice, consult with a qualified attorney
    - Laws change regularly - always verify current legislation
    - Keep records of all legal documents and communications
    """)


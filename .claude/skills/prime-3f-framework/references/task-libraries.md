# Task Libraries, Archetype Matching, and Auto-Scoring

Reference file for the Prime 3F Framework skill. Read this during Free Move 1 (archetype pick), Move 2 (rapid-fire 15), and Move 3 (custom task auto-scoring).

## Keyword Heuristics for Auto-Scoring Custom Tasks

Use these to guess frequency and judgement on custom tasks.

**Frequency signals (default 3, adjust):**
- Words like "daily," "every day," "each morning," "every customer" then set frequency 5
- Words like "weekly," "every week," "standup" then set frequency 4
- Words like "monthly," "quarterly," "end of month" then set frequency 2
- Words like "annually," "once in a while" then set frequency 1

**Judgement signals (default 3, adjust):**
- Words like "template," "standard," "same format," "checklist," "copy-paste," "data entry," "schedule," "remind" then set judgement 1 or 2
- Words like "review," "triage," "summarize," "qualify," "draft" then set judgement 3
- Words like "decide," "negotiate," "price," "hire," "fire," "strategy," "pitch," "present" then set judgement 4 or 5

Show the guesses to the user. Let them flip any.

---

## Archetype Keyword Match Table

Match the role title (case-insensitive) to an archetype.

| Keywords in role | Archetype |
|------------------|-----------|
| coach, coaching, mentor | coach |
| consultant, consulting, advisor, strategist | consultant |
| lawyer, attorney, counsel, paralegal | lawyer |
| cpa, accountant, bookkeeper, tax | cpa |
| realtor, real estate agent, agent, broker | real-estate-agent |
| real estate investor, flipper, wholesaler, landlord | real-estate-investor |
| agency, creative, designer, media buyer, account manager | agency |
| plumber, electrician, contractor, home services, trades, hvac, roofer | service-business |
| course creator, info product, educator, creator | course-creator |
| ecom, ecommerce, shopify, store owner, dtc, brand | ecom |
| saas, software, product manager, founder engineer | saas |
| ceo, founder (team), owner, operator, president (with team of 5+) | prime-operator |
| vp, director, head of, team lead, department lead | prime-leader |
| sales rep, sdr, bdr, account executive | (use agency or consultant sales skew) |
| marketer, content lead, social media manager | (use agency marketing skew) |
| admin, ops, operations, executive assistant | (use prime-leader ops skew) |

Default to `generic` if nothing matches. The `prime-operator` and `prime-leader` archetypes are for $1M to $25M businesses with teams.

---

## Archetype Libraries (Abbreviated)

Each archetype has a 15-task starter list for Move 2 with default frequency (F) and judgement (J) scores. Cover all four quadrants.

### coach (1-on-1 or group coaching, $100K-$2M)

1. Pre-call prep notes (F4, J2)
2. Post-call recap email (F4, J2)
3. Client progress tracking in a spreadsheet (F5, J1)
4. Weekly group content creation (F3, J4)
5. Discovery call (F3, J5)
6. Invoice and payment follow-up (F2, J1)
7. Scheduling and rescheduling (F5, J1)
8. Testimonial collection (F1, J2)
9. Referral ask emails (F2, J2)
10. Client onboarding pack (F2, J2)
11. Social media post drafting (F5, J2)
12. Course module updates (F1, J4)
13. Monthly invoice reconciliation (F1, J1)
14. Client hiring decision (F1, J5)
15. Quarterly strategy pivot (F1, J5)

### consultant ($5K-$50K engagements)

1. Proposal drafting (F3, J3)
2. Weekly client status email (F5, J2)
3. Discovery workshop prep (F2, J4)
4. Deliverable formatting (F4, J1)
5. Meeting notes and action items (F5, J2)
6. Data pull from client's tools (F4, J1)
7. Executive summary writing (F3, J4)
8. Pricing decision (F1, J5)
9. Scope change negotiation (F2, J5)
10. Research brief (F4, J2)
11. Slide deck drafting (F3, J2)
12. Client follow-up cadence (F4, J1)
13. Contract review (F1, J4)
14. Kickoff meeting facilitation (F2, J5)
15. Timesheet logging (F5, J1)

### lawyer (solo or small firm)

1. Client intake triage (F5, J3)
2. Retainer invoice drafting (F3, J1)
3. Document template filling (F5, J1)
4. Case research summary (F3, J4)
5. Court date reminders (F4, J1)
6. Settlement negotiation (F1, J5)
7. Client update emails (F5, J2)
8. Deposition prep (F2, J5)
9. Calendar management (F5, J1)
10. Billable hour tracking (F5, J1)
11. Contract redline first pass (F3, J3)
12. Referral partner outreach (F2, J3)
13. Court filing prep (F3, J3)
14. Client hiring decision (F1, J5)
15. Newsletter drafting (F1, J2)

### cpa (solo or small firm)

1. Client document intake (F5, J1)
2. Tax return data entry (F5, J1)
3. Quarterly estimated tax reminders (F2, J1)
4. Bookkeeping reconciliation (F5, J2)
5. Audit response drafting (F1, J5)
6. Client status update emails (F5, J2)
7. Invoice generation (F4, J1)
8. Schedule planning for tax season (F1, J3)
9. Payroll processing check (F3, J2)
10. Financial statement prep (F3, J3)
11. Tax strategy advice (F2, J5)
12. Referral partner follow-up (F2, J2)
13. Late client reminder emails (F4, J1)
14. Client onboarding pack (F2, J1)
15. Training new staff (F1, J4)

### real-estate-agent

1. Listing description drafting (F4, J2)
2. Open house recap emails (F3, J1)
3. MLS search for clients (F5, J2)
4. Property tour scheduling (F5, J1)
5. Contract drafting from template (F3, J2)
6. Negotiation (F2, J5)
7. Weekly newsletter (F4, J2)
8. Social media post drafting (F5, J2)
9. Referral partner check-in (F3, J2)
10. Closing coordination (F2, J3)
11. Pricing strategy decision (F2, J5)
12. CRM data entry (F5, J1)
13. Client birthday and anniversary emails (F3, J1)
14. Photography coordination (F2, J1)
15. Client hiring decision (F1, J5)

### real-estate-investor

1. Deal analysis spreadsheet (F4, J2)
2. Seller outreach drafting (F5, J2)
3. Property tour scheduling (F3, J1)
4. Contract drafting from template (F2, J2)
5. Lender update emails (F3, J2)
6. Contractor bid comparison (F2, J3)
7. Property listing research (F5, J2)
8. Tenant screening (F3, J4)
9. Lease renewal reminders (F3, J1)
10. Maintenance request triage (F4, J2)
11. Cash flow reporting (F2, J2)
12. Title and escrow coordination (F2, J3)
13. Wholesaler relationship check-in (F3, J2)
14. Acquisition go/no-go decision (F1, J5)
15. Tax strategy (F1, J5)

### agency (marketing, creative, media buying)

1. Client status reports (F5, J2)
2. Ad copy drafting (F5, J2)
3. Creative brief drafting (F4, J3)
4. Campaign performance analysis (F4, J3)
5. Client onboarding pack (F2, J2)
6. Weekly client check-in email (F5, J2)
7. Invoice generation (F4, J1)
8. Proposal drafting (F3, J3)
9. Pricing decision (F1, J5)
10. Content calendar planning (F3, J3)
11. Hire or fire on the team (F1, J5)
12. Social media post drafting (F5, J2)
13. Asset handoff emails (F5, J1)
14. Portfolio case study writing (F1, J3)
15. Kickoff call facilitation (F2, J5)

### service-business (trades, home services)

1. Customer intake calls (F5, J2)
2. Estimate drafting (F5, J2)
3. Scheduling and dispatch (F5, J2)
4. Invoice generation (F5, J1)
5. Customer follow-up emails (F5, J1)
6. Review request texts (F4, J1)
7. Supplier order placing (F4, J1)
8. Crew assignment (F5, J3)
9. Pricing decision (F2, J5)
10. Seasonal promo email (F1, J2)
11. Complaint triage (F3, J4)
12. Truck inventory check (F5, J1)
13. Referral partner thank-you (F2, J1)
14. Hiring decision (F1, J5)
15. Route planning (F5, J2)

### course-creator (info products)

1. Weekly content drafting (F5, J3)
2. Email sequence writing (F3, J3)
3. Student support triage (F5, J2)
4. Sales page copy edits (F2, J4)
5. Module update planning (F1, J4)
6. Webinar prep (F2, J4)
7. Launch email calendar (F2, J3)
8. Affiliate outreach (F2, J2)
9. Testimonial collection (F2, J2)
10. Refund request handling (F3, J3)
11. Social media post drafting (F5, J2)
12. Community post response (F5, J2)
13. Pricing strategy decision (F1, J5)
14. Customer feedback review (F3, J3)
15. New offer design (F1, J5)

### ecom

1. Order fulfillment check (F5, J1)
2. Customer service email triage (F5, J2)
3. Return and refund processing (F5, J2)
4. Product description drafting (F3, J2)
5. Ad copy drafting (F4, J2)
6. Email campaign drafting (F3, J2)
7. Inventory reorder alerts (F4, J1)
8. Review request follow-up (F4, J1)
9. Supplier coordination (F3, J3)
10. Pricing and margin decision (F2, J5)
11. Launch planning (F1, J4)
12. Social media post drafting (F5, J2)
13. Abandoned cart email logic (F3, J3)
14. Influencer outreach (F2, J3)
15. New product pick decision (F1, J5)

### saas

1. Customer support ticket triage (F5, J2)
2. Onboarding email sequence (F3, J2)
3. Churn risk flag reports (F3, J3)
4. Feature request triage (F4, J3)
5. Release notes drafting (F2, J2)
6. Sales demo prep (F4, J3)
7. Invoice and billing follow-up (F4, J1)
8. Product roadmap decisions (F1, J5)
9. Customer success check-in emails (F5, J2)
10. Weekly metrics dashboard update (F5, J2)
11. Pricing page copy edits (F1, J4)
12. Hiring decision (F1, J5)
13. Community post response (F4, J2)
14. Partner outreach (F2, J3)
15. Customer interview note synthesis (F3, J3)

### prime-operator (CEO, founder, owner of $1M-$25M business with a team)

This is the person running the team. Strategic cadence.

1. Weekly scorecard review (F5, J3)
2. Pipeline review with sales lead (F4, J4)
3. L10 or EOS-style team meeting recap (F4, J2)
4. Cash flow forecast update (F3, J3)
5. Hiring scorecard drafting (F2, J4)
6. Exec team weekly briefing (F4, J3)
7. Investor or board update emails (F2, J4)
8. 1-on-1 prep notes (F5, J2)
9. Strategy offsite planning (F1, J5)
10. Client escalation handling (F3, J5)
11. Monthly P&L review (F1, J4)
12. Quarterly OKR setting (F1, J5)
13. Firing decision (F1, J5)
14. Personal calendar triage (F5, J2)
15. Vision and culture comms drafting (F2, J3)

### prime-leader (VP, director, head of function, team lead at $1M-$25M)

Reports to the operator. Tactical cadence.

1. Team performance rollup (F5, J2)
2. Project status digest (F5, J2)
3. Inbound request triage (F5, J2)
4. Hand-off documentation (F4, J2)
5. 1-on-1 agenda drafting (F5, J2)
6. Cross-team update emails (F5, J2)
7. Vendor or tool selection research (F2, J3)
8. Hiring interview scorecards (F2, J4)
9. Budget tracking spreadsheet (F3, J2)
10. Escalation to CEO (F3, J4)
11. Team member performance review (F1, J5)
12. Sprint planning notes (F4, J2)
13. Incident report drafting (F2, J3)
14. Stakeholder update decks (F2, J3)
15. Hiring or firing recommendation (F1, J5)

### generic (fallback)

1. Email triage (F5, J2)
2. Meeting scheduling (F5, J1)
3. Status update writing (F5, J2)
4. Data entry (F5, J1)
5. Report drafting (F3, J2)
6. Customer follow-up emails (F5, J2)
7. Calendar management (F5, J1)
8. Weekly recap email (F4, J2)
9. Research for a project (F3, J2)
10. Deliverable formatting (F4, J1)
11. Task delegation (F4, J3)
12. Client escalation (F2, J5)
13. Proposal drafting (F2, J3)
14. Hiring decision (F1, J5)
15. Strategy call (F2, J5)

---


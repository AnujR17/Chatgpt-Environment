# Refund credit estimates

Checked 17 October 2026 against [Swiggy's public refund policy, D.5](https://www.swiggy.com/refund-policy) and the readable phone screenshots supplied by the user during this review. The public app-oriented and ordinary policy responses matched in the fetch record. All rows below identify the original payment source as the listed refund destination. These are published estimates, not proof of a particular transaction's current provider status.

| Payment method | Listed credit estimate |
| --- | --- |
| Net Banking | 5–7 business days |
| Debit/Credit Cards | 5–7 business days |
| UPI | 5–7 business days |
| Amazon Pay (Wallet) | 5–7 business days |
| Amazon Pay (CC/DC/NB) | 5–7 business days |
| PhonePe (Wallet) | 5–7 business days |
| PhonePe (CC/DC/NB) | 5–7 business days |
| Wallet: Paytm / Mobikwik / Freecharge | 2 hours |
| LazyPay | 2 hours |
| Sodexo | 5–7 business days |

The listed process includes order edits, cancellation, compensation and payment failure. The policy separately mentions choosing an account wallet; do not infer an unlisted wallet-credit time or that every listed method remains available in the current checkout.

## How this should work in the concept

The following are proposed implementation rules, not additional published terms:

1. Read the method and destination from the relevant payment transaction, not the order's generic label alone. Split tenders may have multiple legs.
2. Separate approval from initiation. Until the payment operation is accepted, say approved / awaiting initiation instead of processed.
3. After initiation, show amount, destination, reference, initiation timestamp, provider/policy estimate and an expected range computed with the relevant business-day calendar. Keep absent calendar data explicit.
4. Allow processing, credited, failed and unknown outcomes. If the provider or bank reports a different current estimate, retain both records and show their timestamps rather than overwrite the cited policy silently.
5. A successful payment refunded for food problems is not the same as a failed-payment reversal. Use IN-PAY for the appropriate payment incident; do not apply a blanket food-refund promise to every debit.
6. A source estimate does not change the deadline for accepting/acknowledging a complaint or tracking the grievance. Internal chat reply and handling targets are separate, hypothetical service parameters.

Replace the prototype's universal 3–5-working-day promise with conditional wording. Example proposed copy: Refund initiated: ₹252 to your original UPI payment source. Estimated credit: 5–7 business days. Reference: DEMO-REF-001. If initiation is not confirmed, that wording must not be shown.

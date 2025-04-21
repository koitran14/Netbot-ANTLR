grammar Command;

options { caseInsensitive = true; }

// ==== ENTRY RULE ====
command: greeting* (order | topup)? EOF;

// ==== GREETING ====
greeting: GREETING;

// ==== ORDER RULE ====
order: ORDER_PREFIX? ORDER_AMOUNT ITEM (POLITE)?;

// ==== TOP-UP RULE ====
topup: TOPUP_PREFIX AMOUNT (CURRENCY)? (POLITE)?;

// ==== TERMINALS ====
GREETING: 'hello' | 'hi' | 'hey' | 'good morning' | 'good afternoon';

TOPUP_PREFIX:
      'top up' | 'add money' | 'recharge' | 'fund my account' | 'add to my account' 
    | 'could you add' | 'please top off' | 'i need to put' | 'put some money' | 'load up' 
    | 'can you top up' | 'i want to add' | 'please add' | 'top off my account';

ORDER_PREFIX:
      'order' | 'i want' | 'give me' | 'can i have' | 'please get me' | 'i’d like';

ITEM: 'coffee' | 'tea' | 'pizza' | 'burger' | 'sandwich' | 'soda' | 'water' | 'juice';
ORDER_AMOUNT: [0-9]+;
AMOUNT: [0-9]+ ('.' [0tb-9]+)?; // 12 hoặc 12.5

CURRENCY: 'dollars' | 'usd' | 'vnd';

POLITE: 'please' | 'thanks' | 'thank you';

// ==== SKIP ====
WS: [ \t\r\n]+ -> skip;                            
PUNCTUATION: [.,?!]+ -> skip;                      

grammar Command;

// ==== ENTRY RULE ====
command: greeting* (order | topup)?;

// ==== GREETING ====
greeting: GREETING;

// ==== ORDER RULE ====
order: (ORDER_PREFIX)? ORDER_AMOUNT ITEM (POLITENESS)?;

// ==== TOP-UP RULE ====
topup: TOPUP_PREFIX AMOUNT CURRENCY (account_spec)? (POLITENESS)?;
account_spec: 'to' ('my' 'account' | 'account' ACCOUNT_NAME);

// ==== TERMINALS ====
GREETING: 'hello' | 'hi' | 'hey' | 'good morning' | 'good afternoon';
TOPUP_PREFIX: 'top up' | 'add money' | 'recharge' | 'fund my account' | 'add to my account' 
              | 'could you add' | 'please top off' | 'i need to put' | 'put some money' | 'load up' 
              | 'can you top up' | 'i want to add' | 'please add' | 'top off my account';
AMOUNT: [0-9]+ ('.' [0-9]+)?;
CURRENCY: 'dollars' | 'usd' | 'vnd';
ACCOUNT_NAME: [a-zA-Z][a-zA-Z0-9]*;
ORDER_PREFIX: 'order' | 'i want' | 'give me' | 'can i have' | 'please get me' | 'i’d like';
ORDER_AMOUNT: [0-9]+;
ITEM: 'coffee' | 'tea' | 'pizza' | 'burger' | 'sandwich' | 'soda' | 'water' | 'juice';
POLITENESS: 'thanks' | 'thank you' | 'please';

// ==== SKIP ====
WS: [ \t\r\n]+ -> skip ;                            // Bỏ qua khoảng trắng
PUNCTUATION: [.,?!]+ -> skip;                       // Tạm thời bỏ qua dấu câu
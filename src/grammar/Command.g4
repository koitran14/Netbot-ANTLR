grammar Command;

// Parser rules
command: greeting* (order | topup)?;
greeting: GREETING;
order: ORDER_PREFIX? INTEGER ITEM (POLITE)?;
topup: TOPUP_PREFIX AMOUNT (CURRENCY)? (account_spec)? (POLITE)?;
account_spec: 'to' ('my' 'account' | 'account' ACCOUNT_NAME);

// Lexer rules
// Specific tokens first to avoid conflicts with general tokens
GREETING: 'hello' | 'hi' | 'hey' | 'good morning' | 'good afternoon';
ORDER_PREFIX: 'order' | 'i want' | 'give me' | 'can i have' | 'please get me' | 'i’d like';
TOPUP_PREFIX: 'top up' | 'add money' | 'recharge' | 'fund my account' | 'add to my account' 
              | 'could you add' | 'please top off' | 'i need to put' | 'put some money' | 'load up' 
              | 'can you top up' | 'i want to add' | 'please add' | 'top off my account';
ITEM: 'coffee' | 'tea' | 'pizza' | 'burger' | 'sandwich' | 'soda' | 'water' | 'juice';
POLITE: 'please' | 'thanks' | 'thank you';
CURRENCY: 'dollars' | 'usd';

// General tokens
ACCOUNT_NAME: [a-zA-Z][a-zA-Z0-9]*;

// Unified number token for both integer and decimal amounts
AMOUNT: INTEGER | FLOAT;
INTEGER: [0-9]+;
FLOAT: [0-9]+ ('.' [0-9]+);

// Skip rules
WS: [ \t\r\n]+ -> skip;
PUNCTUATION: [.,?!]+ -> skip;
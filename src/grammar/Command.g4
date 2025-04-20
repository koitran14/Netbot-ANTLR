grammar Command;

command: greeting* (order | topup)?;

greeting: GREETING;

// ORDER GRAMMAR
order: 'Add your grammar';

// TOP-UP GRAMMAR
topup: TOPUP_PREFIX AMOUNT (CURRENCY)? (account_spec)? (POLITE)?;
account_spec: 'to' ('my' 'account' | 'account' ACCOUNT_NAME);

// LEXER RULES
GREETING: 'hello' | 'hi' | 'hey' | 'good morning' | 'good afternoon';
TOPUP_PREFIX: 'top up' | 'add money' | 'recharge' | 'fund my account' | 'add to my account' 
              | 'could you add' | 'please top off' | 'i need to put' | 'put some money' | 'load up' 
              | 'can you top up' | 'i want to add' | 'please add' | 'top off my account';
AMOUNT: [0-9]+ ('.' [0-9]+)?;
CURRENCY: 'dollars' | 'usd' | 'vnd';
POLITE: 'please' | 'thanks' | 'thank you';
ACCOUNT_NAME: [a-zA-Z][a-zA-Z0-9]*;

WS: [ \t\r\n]+ -> skip ;                            // Bỏ qua khoảng trắng
PUNCTUATION: [.,?!]+ -> skip;                       // Tạm thời bỏ qua dấu câu
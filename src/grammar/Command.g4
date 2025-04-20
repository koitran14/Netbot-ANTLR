grammar Command;

command: greeting* (order | topup)?;

greeting: GREETING;

// ORDER
order: 'Add your grammar';

// TOP-UP ACCOUNT
topup: TOPUP_PREFIX AMOUNT (CURRENCY)? (POLITE)?;


// LEXER RULES
GREETING: 'hello' | 'hi' | 'hey' | 'good morning' | 'good afternoon';
TOPUP_PREFIX: 'top up' | 'add money' | 'recharge' | 'fund my account' | 'add to my account' 
              | 'could you add' | 'please top off' | 'i need to put' | 'put some money' | 'load up' 
              | 'can you top up' | 'i want to add' | 'please add' | 'top off my account';
AMOUNT: [0-9]+ ('.' [0-9]+)?;
CURRENCY: 'dollars' | 'usd' | 'vnd';
POLITE: 'please' | 'thanks' | 'thank you';

WS: [ \t\r\n]+ -> skip ;                            // Bỏ qua khoảng trắng
PUNCTUATION: [.,?!]+ -> skip;                       // Tạm thời bỏ qua dấu câu
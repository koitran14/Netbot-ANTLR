grammar Command;

// Parser rules
command: greeting* (order | topup | query_order)?;
greeting: GREETING;

// CHỈNH ĐỂ ORDER NHIỀU MÓN
order: ORDER_PREFIX? item_quantity (CONJ item_quantity)* (POLITE)?;

item_quantity: INTEGER ITEM;

topup: TOPUP_PREFIX amount (CURRENCY)? (account_spec)? (POLITE)?;
amount: INTEGER | FLOAT;
account_spec: 'to' ('my' 'account' | 'account' ACCOUNT_NAME);
query_order: QUERY_ORDER_PREFIX (POLITE)?;

// Lexer rules
GREETING: 'hello' | 'hi' | 'hey' | 'good morning' | 'good afternoon';
ORDER_PREFIX: 'order' | 'i want' | 'give me' | 'can i have' | 'please get me' | 'i’d like';
TOPUP_PREFIX: 'top up' | 'add money' | 'recharge' | 'fund my account' | 'add to my account'
              | 'could you add' | 'please top off' | 'i need to put' | 'put some money'
              | 'load up' | 'can you top up' | 'i want to add' | 'please add' | 'top off my account';
ITEM: 'coffee' | 'tea' | 'pizza' | 'burger' | 'sandwich' | 'soda' | 'water' | 'juice';
QUERY_ORDER_PREFIX: 
    'show my orders' | 'list my orders' | 'show previous orders' | 'list previous orders' | 'what did i order' | 'my order history';
POLITE: 'please' | 'thanks' | 'thank you';
CURRENCY: 'dollars' | 'usd';
CONJ: 'and' | ','; // Cho phép nối các món bằng "and" hoặc dấu ","

ACCOUNT_NAME: [a-zA-Z][a-zA-Z0-9]*;
INTEGER: [0-9]+;
FLOAT: [0-9]+ '.' [0-9]+;

// Skip rules
WS: [ \t\r\n]+ -> skip;
PUNCTUATION: [.,?!]+ -> skip;

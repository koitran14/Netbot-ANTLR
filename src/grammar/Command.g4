grammar Command;

// Parser rules
command: greeting* (order | topup | topupQuery | query_order)?;
greeting: GREETING;

// CHỈNH ĐỂ ORDER NHIỀU MÓN
order: ORDER_PREFIX item_quantity (CONJ item_quantity)* (POLITE)?;

item_quantity: INTEGER ITEM;

topup: TOPUP_PREFIX amount (CURRENCY)? (account_spec)? (POLITE)?;
topupQuery: QUERY_PREFIX (query_type)? ('topup' | 'topups' | 'topup history') (account_spec)? (POLITE)?;
query_type: 'latest' | 'newest' | 'oldest' | 'all';

amount: INTEGER | FLOAT;
account_spec: 'to' ('my' 'account' | 'account' ACCOUNT_NAME);
query_order: QUERY_ORDER_PREFIX (POLITE)?;

// Lexer rules
GREETING: 'hello' | 'hi' | 'hey' | 'good morning' | 'good afternoon';
ORDER_PREFIX: 'order' | 'i want' | 'give me' | 'can i have' | 'please get me' | 'i’d like';
TOPUP_PREFIX: 'top up' | 'top off' | 'add' | 'add money' | 'recharge' | 'fund my account' | 'add to my account' 
              | 'could you add' | 'please top off' | 'i need to put' | 'put some money' 
              | 'load up' | 'can you top up' | 'i want to add' | 'please add' 
              | 'top off my account' | 'i’d like to add' | 'can i add' | 'let’s add' 
              | 'just add' | 'add some' | 'please load' | 'could you top up' 
              | 'i need to add' | 'how about adding' | 'top it up' | 'boost my account' 
              | 'put in' | 'fill up' | 'i want to top up' | 'can we add';
QUERY_PREFIX: 'show' | 'get' | 'list' | 'display' | 'tell me' | 'show me' 
              | 'retrieve' | 'fetch' | 'can i see' | 'can you show' | 'could you list' 
              | 'i want to see' | 'please show' | 'please list' | 'please get' | 'view' 
              | 'check' | 'find' | 'look up' | 'tell me about' | 'what are' | 'what’s' 
              | 'provide' | 'share' | 'pull up' | 'can you tell me' | 'i’d like to see' 
              | 'could you show me' | 'please check' | 'how about' | 'let me see' 
              | 'show the' | 'give me the' | 'i want to check' | 'can i check' 
              | 'tell me the' | 'what about' | 'review' | 'bring up' | 'let’s see';
ITEM: [a-zA-Z]+;
QUERY_ORDER_PREFIX: 
    'show my orders' | 'show my order' | 'list my orders' | 'list my order' | 'show previous orders' | 'show previous order' | 'list previous orders' | 'list previous order' | 'what did i order' | 'my order history';
POLITE: 'please' | 'thanks' | 'thank you';
CURRENCY: 'dollars' | 'usd';
CONJ: 'and' | ','; // Cho phép nối các món bằng "and" hoặc dấu ","

ACCOUNT_NAME: [a-zA-Z][a-zA-Z0-9]*;
INTEGER: [0-9]+;
FLOAT: [0-9]+ '.' [0-9]+;

// Skip rules
WS: [ \t\r\n]+ -> skip;
PUNCTUATION: [.,?!]+ -> skip;

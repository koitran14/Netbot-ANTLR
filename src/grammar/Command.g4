grammar Command;

// Parser rules
command: greeting* (order | topup | topupQuery)?;
greeting: GREETING;
order: ORDER_PREFIX? INTEGER ITEM (POLITE)?;
topup: TOPUP_PREFIX amount (CURRENCY)? (account_spec)? (POLITE)?;
topupQuery: QUERY_PREFIX (query_type)? ('topup' | 'topups' | 'topup history') (account_spec)? (POLITE)?;
query_type: 'latest' | 'oldest' | 'all';

amount: INTEGER | FLOAT;
account_spec: 'to' ('my' 'account' | 'account' ACCOUNT_NAME);

// Lexer rules
GREETING: 'hello' | 'hi' | 'hey' | 'good morning' | 'good afternoon';
ORDER_PREFIX: 'order' | 'i want' | 'give me' | 'can i have' | 'please get me' | 'i’d like';
TOPUP_PREFIX: 'top up' | 'add money' | 'recharge' | 'fund my account' | 'add to my account' 
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
ITEM: 'coffee' | 'tea' | 'pizza' | 'burger' | 'sandwich' | 'soda' | 'water' | 'juice';
POLITE: 'please' | 'thanks' | 'thank you';
CURRENCY: 'dollars' | 'usd';

ACCOUNT_NAME: [a-zA-Z][a-zA-Z0-9]*;

// Unified number token for both integer and decimal amounts
INTEGER: [0-9]+;
FLOAT: [0-9]+ '.' [0-9]+;

// Skip rules
WS: [ \t\r\n]+ -> skip;
PUNCTUATION: [.,?!]+ -> skip;
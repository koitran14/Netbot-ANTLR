grammar Command;

command: greeting* (order | topup | topupQuery | query_order)?;
greeting: GREETING;


topup: TOPUP_PREFIX amount CURRENCY (account_spec)? (POLITE)?;


amount: INTEGER | FLOAT;
INTEGER: [0-9]+;
FLOAT: [0-9]+ '.' [0-9]+;


account_spec: 'to' ('my' 'account' | 'account' ACCOUNT_NAME);


TOPUP_PREFIX: 'top up' | 'top off' | 'add' | 'add money' | 'recharge' | 'fund my account' | 'add to my account' 
              | 'could you add' | 'please top off' | 'i need to put' | 'put some money' 
              | 'load up' | 'can you top up' | 'i want to add' | 'please add' 
              | 'top off my account' | 'i’d like to add' | 'can i add' | 'let’s add' 
              | 'just add' | 'add some' | 'please load' | 'could you top up' 
              | 'i need to add' | 'how about adding' | 'top it up' | 'boost my account' 
              | 'put in' | 'fill up' | 'i want to top up' | 'can we add';



POLITE: 'please' | 'thanks' | 'thank you';


CURRENCY: 'dollars' | 'usd';


ACCOUNT_NAME: [a-zA-Z][a-zA-Z0-9]*;
INTEGER: [0-9]+;
FLOAT: [0-9]+ '.' [0-9]+;




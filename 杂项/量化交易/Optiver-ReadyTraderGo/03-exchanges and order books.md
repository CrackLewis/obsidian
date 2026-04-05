![[Pasted image 20230308135022.png]]

left: bid volumes
mid: price ladders
right: ask volumes

best offer: lowest offer on the sell side
best order: highest order on the buy side
bid ask spread: (best offer - best order)

price time priority:
- ppl with better price have better priority
- given the same price, ppl earlier have better priority

**join**: add volume to specific bid at its lowest priority

**hit the bid**: sell at the existing highest bid price

**lift the order**: buy at the existing lowest ask price in the order book

**dime**/**improve**: add an order which becomes the best bid/offer

![[Pasted image 20230308140639.png]]

**spoofing**:
- sending orders to the order book without having the intention to trade with the order
- this behavior is prohibited by laws and exchanges

![[Pasted image 20230308141727.png]]

order types:
- market order: 
	- one to use with CAUTION
	- by sending it u dont set any cond on the price at which the order will be executed
	- ordering in an illiquid order book could be risky
- limit order:
	- less risky
	- set price condition which limits the max price to buy and the min price to sell
- fill or kill
	- limit order with additional feature: check before entering the order book
	- if can be executed entirely and immediately: fill
	- if not: cancel (kill)
- IOC (immediate or cancel)
	- limit order with additional feature: check before entering the order book
	- only the part which can be executed immediately will be executed
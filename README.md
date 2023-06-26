# deal-finder
We want to know when retail items go on sale. This is a CLI to help scrape different menswear websites for certain matches and sales.

We can search for all products with a minimum discount percentage and get an email with images hyperlinked to their respective product.
```
python3 main.py "pace breaker" -min_discount 20
```
<img width="888" alt="discount_search" src="https://github.com/msanchez-ayala/deal-finder/assets/54561946/d9bc7a82-41c2-40b2-a5bd-3e989480cd6a">

We could alternatively search for full-priced items matching our search terms by omitting `-min_discount`
```
python3 main.py "pace breaker"
```
<img width="974" alt="full_search" src="https://github.com/msanchez-ayala/deal-finder/assets/54561946/d6587f4a-3205-4f3b-b7ca-79c9a461c0d0">




# isadent

This script is meant to indent theory files in Isabelle. The basic usage is as follows:
```bash
isadent Theory.thy > Theory_indented.thy
cat Theory_indented.thy
mv Theory_indented.thy Theory.thy
```
Of course you should check the result instead of trusting it blindly.

This script does not parse the code, it only recognises some keywords and patterns, a bit like Vim does with '='. It will thus fail miserably on complicated theories, although I have only had to add the relevant keywords to make it work again so far.

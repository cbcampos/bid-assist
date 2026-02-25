# BidAssist Development - Common Errors to Avoid

## 1. Duplicate Script Tags
**Problem:** Having multiple `<script>` tags causes JS to execute out of order or merge incorrectly.
**Fix:** Keep all JavaScript in ONE single `<script>` block. Never add additional script tags.

## 2. Broken String Concatenation in Python Replacements
**Problem:** Using complex string replacements with mismatched quotes breaks JS syntax.
**Example:** `old = "...'` + new = "..."` creates invalid JS.
**Fix:** 
- Test regex replacements in isolation first
- Verify brace counts match: `echo "$text" | grep -o '{' | wc -l` should equal `grep -o '}' | wc -l`

## 3. Forgetting to Copy to Static Folder
**Problem:** Edit templates/ but server reads static/
**Fix:** Always run `cp templates/index.html static/index.html` after changes.

## 4. Duplicate Code Blocks (Duplicate Lines)
**Problem:** Running replacement twice adds duplicate `else if` blocks causing syntax errors.
**Fix:** Check for existing code before adding: `grep "pattern" file | wc -l`

## 5. Missing Closing Brackets/Parens
**Problem:** `JSON.stringify(data);` missing `)` - happens when replacing with incomplete strings.
**Fix:** Always verify with `node --check` or count matching parens.

## 6. Browser Cache
**Problem:** Old broken version cached.
**Fix:** Add cache-busting headers or bump version in title.

## Testing Checklist Before Deploying:
1. Check brace balance: `grep -o '{' | wc -l` == `grep -o '}' | wc -l`  
2. Check for duplicate lines: `grep "pattern" file | wc -l`
3. Copy to static folder
4. Test in incognito/private mode

## 7. Always Commit Before Major Changes
**Problem:** Lost full-featured version when repeatedly breaking/restoring.
**Fix:** Commit to git after any significant change so you can restore.

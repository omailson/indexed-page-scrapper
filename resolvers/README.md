# Resolvers

Welcome to the resolvers folder. These are a set of operators that you may find useful to use on your scrapped pages.

When you implement your own scrapper, what you return is a list of dictionaries that can be operated on thanks to the resolvers that are included on this library.

Example resolvers are: filtering, value transformations, custom fields, sorting.

All operators (except sorting) are lazy, i.e. they don't require all pages to be fetched to start operating on.

## Example

Filter by a field in the scrapped document

```python
results = MyScrapper()
pages = (results
    .addResolver(resolvers.Filter(lambda data: data['level'] > 2))
    .execute())
```

See examples in `examples/` folder for better understanding of the resolvers

## List of resolvers

### Counter

Add an auto-increment counter field to each element

#### Example

```python
# Initial data
# {'url': 'john.html', 'name': 'John'}
# {'url': 'mark.html', 'name': 'Mark'}
# {'url': 'alice.html', 'name': 'Alice'}

scrapper = MyScrapper()
elements = (scrapper
    .addResolver(resolvers.Counter('counter'))
    .execute())

for e in elements:
    print e

# Yields to
# {'url': 'john.html', 'name': 'John', 'counter': 0}
# {'url': 'mark.html', 'name': 'Mark', 'counter': 1}
# {'url': 'alice.html', 'name': 'Alice', 'counter': 2}
```

### CustomField

Add a custom field to each element. The value of the field is the return value of a given function

```python
scrapper = MyScrapper()
elements = (scrapper
    .addResolver(resolvers.CustomField('age', lambda data: number_of_years(data['day_of_birth'])))
    .execute())
```

### DownloadFile

Fetch and save a resource referred by a given field. The output location is given by the second argument

#### Example

```python
# Initial data
# {'url': 'john.html', 'name': 'John', 'username': 'john', 'picture': '527bd5b5d689e2c32ae974c6229ff785.jpg'}
# {'url': 'mark.html', 'name': 'Mark', 'username': 'mark', 'picture': 'ea82410c7a9991816b5eeeebe195e20a.jpg'}
# {'url': 'alice.html', 'name': 'Alice', 'username': 'alice', 'picture': '6384e2b2184bcbf58eccf10ca7a6563c.jpg' }

scrapper = MyScrapper()
elements = (scrapper
    .addResolver(resolvers.DownloadFile('picture', lambda data: 'pictures/%s.jpg' % data['username']))
    .execute())

# Since resolvers are lazy operations, you need to iterate over the elements, otherwise no files will be downloaded
for u in elements:
    print 'Downloading %s picture...' % u['username']

# The following files will be created
# pictures/john.jpg
# pictures/mark.jpg
# picture/alice.jpg
```

NOTE: `filename` can also be a string, but keep in mind that it will be overwritten on every iteration (since all elements will save to the same filename)

### DumpJson

Dumps data to a json file given a filename. The filename can be either a string or a function that receives `data` and returns a string.

Any extra arguments are passed on to the `json.dump` function call.

#### Example

```python
# Initial data
# {'url': 'john.html', 'name': 'John', 'username': 'john'}
# {'url': 'mark.html', 'name': 'Mark', 'username': 'mark'}
# {'url': 'alice.html', 'name': 'Alice', 'username': 'alice'}

scrapper = MyScrapper()
elements = (scrapper
    .addResolver(resolvers.DumpJson(filename=lambda data: '%s.json' % data['username']), ensure_ascii=True)
    .execute())

# Since resolvers are lazy operations, you need to iterate over the elements, otherwise no files will be downloaded
for u in elements:
    print 'Dumping %s data...' % u['username']

# The following files will be created:
# john.json
# mark.json
# alice.json
```

### ExcludeFields

Use this resolver if you want some of your fields to be excluded from the final result (eg: the `url` field).

#### Example

```python
# Initial data
# {'url': 'john.html', 'name': 'John'}
# {'url': 'mark.html', 'name': 'Mark'}
# {'url': 'alice.html', 'name': 'Alice'}

scrapper = MyScrapper()
elements = (scrapper
    .addResolver(resolvers.ExcludeFields(['url']))
    .execute())

# Yields to
# {'name': 'John'}
# {'name': 'Mark'}
# {'name': 'Alice'}
```

### Filter

Return only the elements that pass the test implemented by the provided function

#### Example

```python
results = MyScrapper()
pages = (results
    .addResolver(resolvers.Filter(lambda data: data['level'] > 2))
    .execute())
```

### Limit

Limit the returned results to a given number. This is very useful when you're scrapping a very long list of items and just want some of them.

#### Example

Say your page lists 100 users but you're only interested on the first 10. Since this execution is lazy, you don't need to worry if the scrapper will try to download the other 90 users. Hint: it won't.

```python
# Initial data
# ... a very long list of users ...

scrapper = MyScrapper()
users = (scrapper
    .addResolver(resolvers.Limit(10))
    .execute())

for u in users:
    print u

# Only the first 10 users will be fetched
```

### Sort

This is the only non-lazy operator.

*TODO*

### Transform

*TODO*

### WriteFile

*TODO*

## List of abstract resolvers

If you'd like to create your own resolver, you may need to extend from one of the resolvers below

### BaseResolver

As the name says, this is the base resolver. All other resolvers extend from this class.

Resolvers are expected to be lazy operators that will evaluate an iterable. If you're creating a resolver, you'll probably want to keep that in mind.

To extend `BaseResolver` you're required to implement only one method: `resolve(generator)`. Both `Filter` and `Limit` resolvers are good examples on how this works.

Also, you should have some understanding how generators work in python (AKA the `yield` keyword)

### SimpleResolver

*TODO*

### VoidResolver

*TODO*

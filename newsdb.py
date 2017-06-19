#   Database for News
import psycopg2

DBNAME = "news"

RESULT_MAIN = """
<div class="row">
<table class="table table-striped">
  <thead>
    <tr>
      <th class="col-md-6">{fheader}</th>
      <th class="col-md-6 right">{sheader}</th>
    </tr>
  </thead>
  <tbody>
    {inside}
  </tbody>
</table>
</div>
"""

#   First Query to find
#   What are the most popular three articles of all time?
query1 = """\
SELECT  title, count(path) AS total FROM articles, log
WHERE path != '/'
AND path LIKE '%'||articles.slug||'%'
GROUP BY title
ORDER BY total DESC
LIMIT 3
"""

#   Second Query to find
#   Who are the most popular article authors of all time?
query2 = """\
SELECT name, count(path) AS total FROM authors, log, articles
WHERE path != '/'
AND path LIKE '%'||articles.slug||'%'
AND authors.id = articles.author
GROUP BY name
ORDER BY total DESC
"""

#   Third Query to find
#   On which days did more than 1% of requests lead to errors?
query3 = """\
SELECT DATE(time),
ROUND(SUM(CASE log.status WHEN '200 OK' THEN 0 ELSE 1 END) * 100.0
/COUNT(log.status),4) AS error_rate
FROM log
GROUP BY DATE(time)
HAVING(SUM(CASE log.status WHEN '200 OK' THEN 0 ELSE 1 END) * 100.0/
COUNT(log.status)) > 1
"""


def get_result(query):
    """ Connect to the DB and return the result from the provided query """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    result = c.fetchall()
    db.close()
    return result


#   A single query result html template
RESULT_TD = """
    <tr>
        <td class="col-md-6">{content_1}</td>
        <td class="col-md-6 right">{content_2}</td>
    </tr>
"""


def result_to_view(number):
    """ This function returns query result in HTML format """
    content = ''

    #  If parameter is 1, then set the query and heading values
    #  as related to the first query, then execute
    if number == 1:
        query = query1
        header1 = "Article Name"
        header2 = "Views"

    #  If parameter is 2, then set the query and heading values
    #  as related to the second query, then execute
    elif number == 2:
        query = query2
        header1 = "Author Name"
        header2 = "Page Views"

    #  If parameter is not 1 or 2, then set the query and heading values
    #  as related to the third query, then execute
    else:
        query = query3
        header1 = "Date"
        header2 = "Error Rate (%)"

    #  Store query result to result
    result = get_result(query)

    #  Append the query result with its content filled in
    for row in result:
        content += RESULT_TD.format(
            content_1=row[0],
            content_2=row[1],
        )

    # Append headers and replace inside placeholder generated content
    rendered_content = RESULT_MAIN.format(
        fheader=header1,
        sheader=header2,
        inside=content
    )

    return rendered_content

def print_query(f, query, num):
    if num == '1':
        title = 'What are the most popular three articles of all time?\n'
        last = ' views'
    elif num == '2':
        title = 'Who are the most popular article authors of all time?\n'
        last = ' views'
    else:
        title = 'On which days did more than 1% of requests lead to errors?\n'
        last = ' %'

    f.write('\n' + str(title) + '\n')
    for result in query:
        f.write(str(result[0]) + ' ----------------- ' + str(result[1]) + last + ' \n')


def print_output():
    f = open('result.txt','w')
    result1 = get_result(query1)
    result2 = get_result(query2)
    result3 = get_result(query3)

    print_query(f,result1,'1')
    print_query(f,result2,'2')
    print_query(f,result3,'3')
    f.close()

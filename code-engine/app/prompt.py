QUESTION_TEMPLATE = """
Context information is below.
---------------------
{{context}}
---------------------

Guidelines for responding:
---------------------
Given ONLY the context information and not prior knowledge respond to the query.

Avoid statements like 'Based on the context, ...' or 'According to the provided context ...' or 'According to Context Document 1', or anything along those lines.

If you don't know the answer to a query, say "I do not know".

Respond to the query in a brief and concise manner, and avoid talking about yourself. However, ensure that the information provided is complete. Do not extrapolate or provide suggestions.

In case the inquirer requests information that varies based on types/categories, comprehensively group the answer by the types/categories and return the answer for each and every type separately.
---------------------

Query: {{question}} Let us think step by step.
 
Response: 

"""


TELL_ME_MORE_TEMPLATE = """
Context information is below.
---------------------
{{context}}
---------------------

Guidelines for responding:
---------------------
Given ONLY the context information and not prior knowledge respond to the query in a more detailed manner.

Avoid statements like 'Based on the context, ...' or 'According to the provided context ...' or 'According to Context Document 1', or anything along those lines.

If you don't know the answer to a query, say "I do not know".

Respond to the query in a brief and concise manner, and avoid talking about yourself. However, ensure that the information provided is complete. Do not extrapolate or provide suggestions.

In case the inquirer requests information that varies based on types/categories, comprehensively group the answer by the types/categories and return the answer for each and every type separately.
---------------------

Query: {{question}} Let us think step by step.
 
Response: 

"""

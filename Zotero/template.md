---
{% if title %}Title: "{{title}}"{% endif %}
Authors: {{authors}}{{directors}}
{% if publicationTitle %}Publication: "{{publicationTitle}}"{% endif %}
{% if date %}Date: {{date | format("YYYY-MM-DD")}}{% endif %}
citekey: {{citekey}}
tags: {{hashTags}}
---
## {{title}}

**引文目录:** {{bibliography}}

**来源:** {{url}}

**Zotero 位置:** {{pdfZoteroLink}}

**Tags :** {{hashTags}} 

>[!abstract]+
>*« {{abstractNote}} »*

{% for annotation in annotations -%}
>[!Annotation|{{annotation.color}}]+ 
>{%- if annotation.annotatedText -%}*« {{annotation.annotatedText}} »*([{{annotation.page}}](zotero://open-pdf/library/items/{{annotation.attachment.itemKey}}?page={{annotation.page}}&annotation={{annotation.id}})){% endif %}{% if annotation.imageRelativePath %}![[{{annotation.imageRelativePath}}]]{% endif %}{% if annotation.comment %} 
>
>{{annotation.comment}}{%- endif %}

{% endfor %}
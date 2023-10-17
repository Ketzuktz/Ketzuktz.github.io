from lxml import etree, html

html_string = '<p style="white-space: pre-wrap;">造成2点\
<strong><u>物理伤害</u></strong>\
<span data-type="详情" data-name="&lt;p style=&#34;\
white-space: pre-wrap;&#34;&gt;\
&lt;strong&gt;物理伤害&lt;/strong&gt;\
&lt;/p&gt;&lt;p style=&#34;white-space: pre-wrap;&#34;&gt;\
物理伤害不会附着元素，也不会发生元素反应。\
&lt;/p&gt;" class="wiki-note-text">\
<sup class="wiki-sup">[详情]</sup></span>。</p>'

# 创建lxml Element对象
root = etree.fromstring(html_string)

skill_description = ''.join(root.xpath('//*[not(self::sup)]/text()')).strip()

# 创建词典来存储加粗文本和详情
bold_text_dict = {}

# 查找所有包含 "strong" 的文本
strong_elements = root.xpath(".//strong//text()")
for element in strong_elements:
    # 获取加粗文本
    bold_text = element.strip()
    if bold_text:
        # 检查是否有相邻的 span 元素包含正确的 data-type 和 data-name 属性
        next_element = element.getparent().getparent().getnext()
        if (
            next_element is not None
            and next_element.tag == "span"
            and next_element.get("data-type") == "详情"
        ):
            # 获取详情文本
            detail_text = next_element.get("data-name")
            bold_text_dict[bold_text] = detail_text

# 打印技能描述和词典
print("技能描述:", skill_description)
for bold_text, detail_text in bold_text_dict.items():
    parsed_html = html.fromstring(detail_text)
    title = parsed_html.xpath('//strong/text()')[0]
    content = parsed_html.xpath('//p[@style="white-space: pre-wrap;"]/text()')[0]

    assert title == bold_text
    print(f"{bold_text}: {content}")

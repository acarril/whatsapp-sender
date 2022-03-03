import re

def custom_message_from_template(template_text:str, fields:list=['foo', 'bar']) -> str:
    # Define regex pattern to look for in template
    # These are the Twilio-style fields to be replaced, with format {{1}}, {{2}}, etc. 
    pattern = r"\{(?<=\{).*?(?=)\}\}"
    # Verify that `template_text` has same numbe of fields as list in `fields`
    if len([*re.finditer(pattern, template_text)]) != len(fields):
        raise ValueError("length of fields must be equal to number of replacements in the template")
    # Construct a mapping from Twilio-style inputs to fields for replacement
    fields_map = dict(
        zip(
            ['{{'+str(x)+'}}' for x in range(1, len(fields)+1)],
            fields
        )
    )
    # Return message with substitutions using fields map
    return re.sub(pattern, lambda x: fields_map[x.group()], template_text)

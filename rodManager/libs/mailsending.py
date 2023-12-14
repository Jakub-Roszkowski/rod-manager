from django.core.mail import EmailMultiAlternatives


def send_mail_from_template(template_name, subject, to, data):
    if not isinstance(to, list):
        to = [to]
    new_to = []
    for email in to:
        if (
            email.endswith("@gmail.com")
            or email.endswith("@wp.pl")
            or email.endswith("@onet.pl")
            or email.endswith("@plociennik.info")
        ):
            new_to.append(email)
    to = new_to
    if len(to) == 0:
        print("No valid email addresses.")
        return None

    from_email = "rodzinneogrodkidzialkowe@gmail.com"
    try:
        with open(f"rodManager/template/email/{template_name}.html") as f:
            template = f.read()
        with open(f"rodManager/template/email/{template_name}.txt") as f:
            simple_template = f.read()
    except FileNotFoundError:
        raise Exception("Template not found.")
    for key, value in data.items():
        placeholder = "{{" + key + "}}"
        template = template.replace(placeholder, value)
        simple_template = simple_template.replace(placeholder, value)
    msg = EmailMultiAlternatives(subject, simple_template, from_email, to)
    msg.attach_alternative(template, "text/html")
    msg.send(fail_silently=False)

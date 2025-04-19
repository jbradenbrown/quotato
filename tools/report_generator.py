def generate_report(vendors: list, responses: dict, filepath="report.md"):
    with open(filepath, "w") as f:
        f.write("# 🥔 Quotato Quote Report\n\n")
        for v in vendors:
            name = v['name']
            f.write(f"## {name}\n")
            if 'email' in v:
                f.write(f"- Email: {v['email']}\n")
            if 'form_url' in v:
                f.write(f"📍 [Online Form]({v['form_url']})\n")
            f.write(f"📝 Response: {responses.get(name, 'No response')}\n\n")

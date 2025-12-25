import os
from datetime import datetime
from dotenv import load_dotenv

from sonarqube.parser import fetch_sonar_issues, sonar_summary
from notify.tg import TelegramNotifier

load_dotenv()


def build_md_report(project, version, author, mr, tag, docker_image, summary, status):
   
    return f"""
🆕 *Новый выпуск изменений*

*Проект:* `{project}`
*Версия:* `{version}`
*Дата:* `{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}`
*Автор:* `{author}`

*Информация о Git-репозитории*
GIT MR: `{mr}`
GIT TAG: `{tag}`

*Информация о Docker-репозитории*
Полное имя: `{docker_image}`

*SonarQube Code Quality*
BLOCKER: `{summary['BLOCKER']}`
CRITICAL: `{summary['CRITICAL']}`
MAJOR: `{summary['MAJOR']}`
MINOR: `{summary['MINOR']}`
INFO: `{summary['INFO']}`

*Статус:* `{status}`
"""


def main():

    issues = fetch_sonar_issues(
        os.getenv("SONAR_URL"),
        os.getenv("SONAR_TOKEN"),
        os.getenv("SONAR_PROJECT_KEY")
    )


    summary, status = sonar_summary(issues)

    notifier = TelegramNotifier(
        os.getenv("TELEGRAM_TOKEN"),
        os.getenv("TELEGRAM_CHAT_ID")
    )

    message = build_md_report(
        project="User_app",
        version="v1.0.0",
        author="karenovnameriko",
        mr="147",
        tag="v1.0.0",
        docker_image="karenovnameriko/user-app:v1.0.0",
        summary=summary,
        status=status
    )

    notifier.send_message(message)
    notifier.send_file("changelog.md")


if __name__ == "__main__":
    main()

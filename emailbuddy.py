from exchangelib import Configuration, Account, Credentials
from exchangelib.indexed_properties import EmailAddress
import pandas as pd
import re
import requests
import dateutil.tz
from datetime import datetime
import pytz
from textblob import TextBlob
from exchangelib import EWSTimeZone, EWSDateTime, EWSDate, UTC, UTC_NOW
import os
import seaborn as sns
import openai
import re
import logging
import sqlite3
from typing import List
from IPython.display import display, clear_output, Javascript, HTML
from ipywidgets import Button, Output, HBox, Textarea, Checkbox, widgets
import mysql.connector


# Move_mail define Emails to be sorted into specific Mail Folders
move_email = {
    "IMPORTANT": [
        "orietta.emiliani@nhs.net",
        "cameron.mcivor@nhs.net",
        "rekha.jayatissa@nhs.net",
        "burhanaliadib@gmail.com",
        "fiona.butler@nhs.net",
        "anna.cantlay@nhs.net",
        "ccsm@nhsdigital.nhs.uk",
        "s.ramtale@imperial.ac.uk",
        "alex.florko@nhs.net"
    ],
    "The Good Practice 2": [
        "thegoodpractice2@nhs.net",
        "cameron.mcivor@nhs.net",
        "claire.perez4@nhs.net",
        "justinhammond@nhs.net"
    ],
    "Earls Court Surgery": [
        "isma.moosa@nhs.net",
        "joyce.frankson@nhs.net",
        "christinehyppolite@nhs.net",
        "lula.eyasu@nhs.net",
        "rinku.patel1@nhs.net",
        "Kate@rbp.co.uk",
        "cqrs.support@nhs.net"
    ],
    "NWL ICS GP Fed": [
        "nhsnwl.westlondongpfederation@nhs.net",
        "helen.tsang@nhs.net",
        "nwl.infogovernance@nhs.net",
        "donna.hislop@nhs.net",
        "nhsnwl.localservices@nhs.net",
        "nhsnwl.wlprimarycare@nhs.net",
        "nhsnwl.lon-nw-pcc@nhs.net",
        "nhsnwl.covidvaccination@nhs.net",
        "nhsnwl.wlmedicinesmanagement@nhs.net",
        "nhsnwl.servicedesk@nhs.net"
    ],
    "PCN": [
        "krydings@nhs.net",
        "maryla.karge@nhs.net",
        "maria.pankhurst@nhs.net",
        "warwick.young@nhs.net",
        "katarzyna.sroga@nhs.net",
        "marzena.grzymala@nhs.net",
        "lesley.french@nhs.net",
        "zaby.begum@nhs.net",
        "e.etim-offiong@nhs.net",
        "thomas.newland1@nhs.net",
        "dana.camino@nhs.net",
        "jas.dua@nhs.net",
        "paul.carnduff@nhs.net"
    ],
    "Clinical Research": [
        "lnw.primarycare@nihr.ac.uk",
        "jalpa.bajaria@nihr.ac.uk",
        "antoinetr.ac.uk",
        "ashnee.dhondete.mcnulty@nihe@nihr.ac.uk",
        "carbis_hannah@lilly.com",
        "summits@myscrs.org",
        "communications@myscrs.org",
        "s.ramtale@imperial.ac.uk",
        "matt.glasier@onestudyteam.com",
        "lauren.gledhill@informa.com",
        "n.e.bailey@soton.ac.uk",
        "nhsnwl.westlondon.trainingandresearch@nhs.net",
        "nhsnwl.westlondon.research@nhs.net"
    ],
    "The Chelsea Practice": [
        "k.shackleford@nhs.net",
        "alexander.johnston1@nhs.net",
        "claire.scudder@nhs.net",
        "marius.brill@nhs.net",
        "k.e.wisniewska@soton.ac.uk",
        "ph204@leicester.ac.uk",
        "ra421@leicester.ac.uk",
        "helen.dallosso@uhl-tr.nhs.uk"
    ],
    "Jan Special Interest": [
        "info@make.com",
        "colin.paget@hn-company.co.uk",
        "jan.duplessis@nhs.net",
        "jpltuk@aol.com",
        "jack.clitheroe@azets.co.uk",
        "rick.smith@forbesburton.com",
        "nicholas.troth@forbesburton.com"
    ],
    "Admin Tasks": ["mail@treeviewdesigns.thirdparty.nhs.uk"],
    "Finance": [
        "sales@medical-supermarket.com",
        "info@email.bionic.co.uk",
        "nisha@rbp.co.uk",
        "sc-invoices@southern-comms.co.uk",
        "shared.services2@nhs.net",
        "support@lantum.com"
    ],
    "PCSE": [
        "pcse.rejectedregistrations@nhs.net",
        "pcse.csc-noreply@nhs.net",
        "donotreply@pcsengland.co.uk"
    ],
}


# Junk Mail Subject Lines
subject_scan = [
    "a bigger",
    "and more",
    "approved",
    "as seen",
    "at no cost",
    "black friday",
    "Black Friday",
    "Change of Contact Details",
    "cheap",
    "Check Your Bill",
    "contact us form",
    "discount",
    "Do you have",
    "Don't miss out",
    "entrepreneurs",
    "for you",
    "GPs available",
    "Get PAID",
    "Hamper",
    "Hampers",
    "Locum",
    "Locum available",
    "low rates",
    "new",
    "offer",
    "potential candidates",
    "Recommended Training",
    "real python",
    "register now",
    "repeat prescription request",
    "sale",
    "season\’s greetings",
    "security measures",
    "SMS from",
    "Suitable opportunities",
    "The Healthcare",
    "your bills",
    "your family",
]


# Junk Mail Subject Lines
blacklisted = [
    "weekly-insights@ecommercedb.com",
    "barbara.little@takepayments.com",
    "noreply@tegliveeurope.com",
    "info@realpython.com",
    "katharina.buchholz@statista.com",
    "Philip.West@keymedicalservices.co.uk",
    "noreply@yammer.com",
    "m.kleinschmidt@statista.com",
    "nheevent@cognitivepublishing.co.uk",
    "info@cdisc.org",
    "printers@practicesupplies.co.uk",
    "e-learning@peninsula-communications.com",
    "training@governmentexchange.co.uk",
    "hayden@thegpagency.co.uk",
    "hugo.norris-mitson@wesleyan.co.uk",
    "noreply@sp.eocampaign1.com",
    "tracy@generalpracticetrainingltd.co.uk",
    "info@switch-us.co.uk",
    "linda@thegbexpos.co.uk",
    "raja.khan@thegpteam.co.uk",
    "vault-emails@veeva.com",
    "will.drake@keymedicalservices.co.uk",
    "hello@utilitycentre.co.uk",
    "news@cognitivepublishing.co.uk",
    "info@rdforum.org.uk",
    "emails@bluestreamacademy.com",
    "marketing@intermedical.co.uk",
    "noreply@mail4.appliancesdirect.co.uk",
    "noreply@nhsbsa.nhs.uk",
    "infouk@medicaldirector.com",
    "newsletter@ourworldindata.org",
    "gp.education@cromwellhospital.com",
    "jmolloy@hg-ahp.com",
    "offers@tradepubs.nl00.net",
    "emma@pcmchambers.co.uk",
    "no.reply@m.email.hostelworld.com",
    "mazars@mazars.co.uk",
    "campaigns@govnewsdirect.com",
    "events@thelondonclinic.co.uk",
    "r.mckinson@thelondonclinic.co.uk",
    "noreply@dam-health.com",
    "kirby@shrgroup.uk",
    "daniel.jones@keymedicalservices.co.uk",
    "maria.axford@pcc-cic.org.uk",
    "pc@intermedical.co.uk",
    "hello@livi.co.uk",
    "info@menloparkrecruitment.com",
    "betsyk@jifjaff.co.uk",
    "irt.support@medpace.com",
    "chardon@research.exafield.com",
    "communications@castoredc.com",
    "lynn@thegpagency.co.uk",
    "info@smartmail.quadient.com",
    "rodger@thegbexpos.co.uk",
    "no-reply@ubibot.com",
    "professionals@prostatecanceruk.org",
    "survey@experience.microsoft.com",
    "conferences@publicpolicyexchange.co.uk",
    "info@hscmon1.co.uk",
    "events@mail1.westminster-insight.com",
    "harry@charitiesbuyinggroup.com",
    "imperial@info.emeritus.org",
    "simon@locummeds.co.uk",
    "noreply@wilmingtonplc.com",
    "info@cdisc.org",
    "nheevent@cognitivepublishing.co.uk",
    "info@menloparkrecruitment.com",
    "E-learning@peninsula-communications.com",
    "g.crowther@medpace.com",
    "zakariya@locummedsgp.co.uk",
    "emma@pcmchambers.co.uk",
    "info@oscarresearch.co.uk",
    "NHEEvent@cognitivepublishing.co.uk",
    "healthservicejournal@hsj.co.uk",
    "Prabhjoat.Riyat@LiquidPlc.com",
    "infographics@statista.com",
    "ubereats@uber.com",
    "infographics@statista.com",
    "hello@onestudyteam.com",
    "Prabhjoat.Riyat@LiquidPlc.com",
    "no_reply@info3.giffgaff.com",
    "Offers@Tradepubs.nl00.net",
    "info@governmentexchange.co.uk",
    "gppact@gmail.com",
    "martin.armstrong@statista.com",
    "CQC@public.govdelivery.com",
    "feedback@qlik.com",
    "Offers@Tradepubs.nl00.net",
    "ubereats@uber.com",
    "hello@onestudyteam.com",
    "contact-maketing@statista.com",
    "spencer@lastminute-locum.co.uk",
    "events@mail.westminster-insight.com",
    "bulletins@em.gpbusiness.co.uk",
    "cassie.hayne@governmentevents.co.uk",
    "customers@portmanassetfinance.co.uk",
    "bobby.brown@governmentevents.co.uk",
    "R.McKinson@thelondonclinic.co.uk",
    "ben@shrgroup.uk",
    "sterlingeventsteam@gmail.com",
    "paul.jones@quadient.com",
    "Info@menloparkrecruitment.com",
    "Emma@pcmchambers.co.uk",
    "ryan@pc-nursing.co.uk",
    "douglas.mason@evolutio-uk.com",
    "learn@asana.com",
    "hello@email.cv-library.co.uk",
    "lexacom@GP.newsme.uk",
    "C.Ash@thelondonclinic.co.uk",
    "callcare247.activehosted.com@s5.csa1.acemsa1.com",
    "team@gaylondonlife.co.uk",
    "bookingsteam@langleyclarkrecruitment.com",
    "theteam@primarycareit.co.uk",
    "hello@keylocums.com",
    "L.Pitts@Medpace.com",
    "jack@lastminute-locum.co.uk",
    "maria.penn@numednews.co.uk",
    "nathan.cole@practicesupplies.co.uk",
    "gps.info@prospect-health.com",
    "isaac@pcmchambers.co.uk",
    "info@uniqskills.co.uk",
    "quickbooks@notification.intuit.com",
    "PSEEvent@cognitivepublishing.co.uk",
    "emily.marie@governmentevents.co.uk",
    "picks@campaign.eventbrite.com",
    "invitation@online1.snapsurveys.com",
    "J.Gooch@thelondonclinic.co.uk",
    "raz@pairoo.com",
    "news@email.bmalaw.co.uk",
    "PrioryNews@priorygroup.com",
    "news@email.bmalaw.co.uk",
    "azure@email.microsoft.com",
    "news@advarra.com",
    "broomwell@GP.newsme.uk",
    "julia.gomez@smetoday-news.co.uk",
    "john@sme-today.co.uk",
    "sales@panacealogic.com",
    "laura@cvevents.co.uk",
    "gp@totalassist.co.uk",
    "safetysubmissionsPA@medpace.com",
    "Hugo.Norris-Mitson@wesleyan.co.uk",
    "education@hje.org.uk",
    "chealy@wilsonbrowne.co.uk",
    "thepensionsregulator@tpr.gov.uk",
    "conferences@ccclimited-mail.org.uk",
    "azure-noreply@microsoft.com",
    "no-reply@wilsonbrowne.co.uk",
    "newenquiries@wilsonbrowne.co.uk",
    "notifications@barclaycarddatasecuritymanager.co.uk",
    "no-reply@anaconda.cloud",
    "qlikwebinars@qlik.com",
]


# Forwarding emails data - KEY: Forwarding Eamil Address VALUE: Identify Mail to move by email or subject line.
forward_mail_dict = {
    "info@realpython.com": "drjanduplessis@icloud.com",
    "newsletter@ourworldindata.org": "drjanduplessis@icloud.com",
    "mail@treeviewdesigns.thirdparty.nhs.uk": "thegoodpractce2@nhs.net",
}

forward_mail_dict_subject = {"E87762": "cameron.mcivor@nhs.net"}


class EmailBuddy:
    def __init__(self):
        self.setup_logger()
        self.connect_ebmysql()

    def connect_ebmysql(self):
        host2 = "sql8.freesqldatabase.com"
        database2 = "sql8612718"
        username2 = "sql8612718"
        password2 = "twkFqs7EWl"
        self.cnx2 = mysql.connector.connect(
            user=username2, password=password2, host=host2, database=database2
        )
        self.cursor2 = self.cnx2.cursor(buffered=True)

    def add_to_blacklist(self, email):
        if email != "":
            query = "SELECT * FROM blacklisted_emails WHERE email = %s"
            self.cursor2.execute(query, (email,))

            if self.cursor2.fetchone() is not None:
                return f"Email {email} already exists in the database."

            add_email = "INSERT INTO blacklisted_emails " "(email) " "VALUES (%s)"
            self.cursor2.execute(add_email, (email,))
            self.cnx2.commit()

            return f"Email {email} has been successfully added to the blacklist."
        else:
            print("Please enter a valid email address.")

    def add_blacklist(self):
        """
        Displays an input field for an email and a button to add the email to the blacklist.
        """
        email_input = widgets.Text(
            value="", placeholder="Enter email", description="Email:", disabled=False
        )
        add_button = widgets.Button(description="Add Email")
        add_button.style.button_color = (
            "lightblue"  # you can change the color to match your preferences
        )

        # Define the on_click event handler
        def on_add_click(_):
            email = email_input.value
            msg = self.add_to_blacklist(email)
            print(msg)
            email_input.value = ""

        # Attach the event handler to the button
        add_button.on_click(on_add_click)

        # Display the button
        display(HBox([email_input, add_button]))

    def setup_logger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # console_handler = logging.StreamHandler()
        # console_handler.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler("email_buddy.log")
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        # console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def authenticate(self):
        # nhsemail = os.environ.get("NHS_EMAIL")
        # nhspassword = os.environ.get("NHS_PASSWORD")
        nhsemail = 'jan.duplessis@nhs.net'
        nhspassword = 'Codefox9876@-5325'
        credentials = Credentials(username=nhsemail, password=nhspassword)
        config = Configuration(server="outlook.office365.com", credentials=credentials)
        self.account = Account(
            primary_smtp_address=nhsemail,
            config=config,
            autodiscover=True,
            access_type="delegate",
        )
        self.logger.info(f"❗️ Authentication successful")
        self.logger.info(
            f"Mailbox: {self.account.primary_smtp_address} - Inbox Count: {self.account.inbox.total_count}"
        )
        unread_in_inbox = self.account.inbox.filter(is_read=False)
        count = unread_in_inbox.count()
        print(
            f"🔌 Mailbox: {self.account.primary_smtp_address} - {count}/{self.account.inbox.total_count} unread"
        )
        return self.account

    def important_email_webhook(self, subject, summary, text_body, email_address):
        url = "https://hook.eu1.make.com/vs2f72qgwqump6g5dc9pthtorw2u8lii"

        payload = {
            "subject": subject,
            "summary": summary,
            "text_body": text_body,
            "email_address": email_address,
        }

        response = requests.post(url, payload)

        if response.status_code == 200:
            print("Webhook sent successfully!")
        else:
            print("Failed to send webhook. Status code:", response.status_code)

    def email_to_folder(self, move_mail):
        self.logger.info(f"✔️ Run function - email_to_folder")

        move_count = 0
        progress_bar = widgets.IntProgress(
            value=0, min=0, max=10, description="👩‍🏫 Reading"
        )
        label = widgets.Label(value="")

        # display them
        display(widgets.HBox([progress_bar, label]))

        for i, (folder, email) in enumerate(move_email.items()):
            e_list = list(email)
            # Update progress bar
            progress_bar.value = i + 1
            label.value = f"Folder: {i} {folder}"
            for e in e_list:
                items = self.account.inbox.filter(f"from:{e}")

                for item in items:
                    body = item.text_body
                    pattern = r"(?:<https?://\S+>)|(?:</?url=[^>]+>)|\[http://links\.haymarket\.mkt6316\.com/eos/v1/[^]]+\]"
                    clean_body = re.sub(pattern, "", body)
                    clean_body = clean_body.replace("\r", "")
                    clean_body = clean_body[:3900]
                    subject = item.subject

                    # # Generate summary of email text body using OpenAI API
                    # openai.api_key = os.environ.get("OPENAI_API_KEY")
                    # prompt = (
                    #     f"Only consider the top email in the email chain. Please provide a succinct summary of the provided email text (top email only), condensing its main points into 2-3 sentences. Ensure that your summary is clear and comprehensive enough to understand the email's content without needing to refer back to the original text. Also, identify any tasks or action items mentioned in the email and list them separately under the heading '❗️Action Required', insert a new line before '❗️Action Required'. Be sure to omit email footers and any information from paragraphs that start with 'This message originated from outside of NHSmail'. Your aim is to provide a brief yet informative snapshot of the email for those who may not have time to read the full text.:\n"
                    #     f"{clean_body}"
                    # )
                    # response = openai.Completion.create(
                    #     engine="text-davinci-002",
                    #     prompt=prompt,
                    #     max_tokens=300,
                    #     n=0.8,
                    #     stop=None,
                    #     temperature=0.7,
                    # )
                    # summary = response.choices[0].text.strip()

                    summary = 'ChatGPT not avaialble'
                    move_count = move_count + 1
                    # Print summary
                    self.logger.info(
                        f"🔸 {subject} from {item.sender.email_address} Summary: {summary}"
                    )
                    print(
                        f"\n🔸 {subject} from {item.sender.email_address}\nSummary: {summary}"

                    )
                    self.important_email_webhook(
                        subject, summary, clean_body, item.sender.email_address
                    )

                    execute = self.account.inbox.filter(f"from:{e}").move(
                        to_folder=self.account.inbox / folder
                    )
                    if not execute:
                        pass
                    else:
                        self.logger.info(f"🔺 📂 {folder} ⬅︎ {e}")
                        print(f"\n📂 {folder} ⬅︎ {e}\n")

        if move_count == 0:
            self.logger.info(f"Zero Emails moved.clear")
        else:
            self.logger.info(f"↩️ Emails moved: {move_count}")

    def folder_review(self):
        email_folders = [
            "IMPORTANT",
            "Inbox-cc",
            "Earls Court Surgery",
            "NWL ICS GP Fed",
            "PCN",
            "Clinical Research",
            "The Chelsea Practice",
            "Jan Special Interest",
            "PCSE",
        ]

        progress_bar = widgets.IntProgress(
            value=0, min=0, max=len(email_folders), description="📁 Folders"
        )
        label = widgets.Label(value="")

        # display them
        display(widgets.HBox([progress_bar, label]))

        for i, folder in enumerate(email_folders):
            # Update progress bar
            progress_bar.value = i + 1
            label.value = f"Folder: {i}. {folder}"

            subfolder = self.account.inbox / folder

            # Filter emails in subfolder that are unread
            unread_emails = subfolder.filter(is_read=False)

            # Count the number of unread emails
            unread_count = unread_emails.count()
            print(f"\n📁 {folder}: {unread_count} unread ")

            for j, unread in enumerate(unread_emails):
                subject = unread.subject
                email_address = unread.sender.email_address
                print(f"{j+1}. {subject} → {email_address}")

    def delete_by_sender(self):
        self.logger.info(f"✔️ Run function - Delete by Sender")
        query = "SELECT email FROM blacklisted_emails"
        # Execute the query
        self.cursor2.execute(query)
        # Get all blacklisted emails
        blacklisted_emails = [row[0] for row in self.cursor2.fetchall()]
        count = 0
        email_list_len = len(blacklisted_emails)
        self.logger.info(f"Blacklisted emails: {email_list_len}")

        progress_bar = widgets.IntProgress(
            value=0, min=0, max=email_list_len, description="❌ Deleting Junk"
        )
        label = widgets.Label(value="")

        # display them
        display(widgets.HBox([progress_bar, label]))

        for i, email in enumerate(blacklisted_emails):
            filtered_items = self.account.inbox.filter(sender__contains=email)
            for item in filtered_items:
                count += 1
                self.logger.info(
                    f"❌ Deleted Email from {item.sender.email_address} - {item.subject}"
                )
                print(
                    f"❌ Deleted Email from {item.sender.email_address} - {item.subject}"
                )
                item.move(to_folder=self.account.trash)

            # Update progress bar
            progress_bar.value = i + 1
            label.value = f"Iteration {i+1}"

        self.logger.info(f"Emails deleted {count}")

    def make_email_list(self):
        self.logger.info(f"✔️ Generating Inbox Email List \n")
        print(
            f"\n✔️ Inbox Summary ______________________________________________________________________\n"
        )
        emaill = []
        subjectl = []
        count = 1

        for item in self.account.inbox.all().order_by("-datetime_received"):
            subject = item.subject
            email = item.sender.email_address
            emaill.append(email)
            subjectl.append(subject)
            print(f"{count}. {subject} → {email}")
            count = count + 1
        print()
        self.logger.info(f"Inbox email_list {emaill}")


    def sentiment_a(self, text_body):
        classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        sent = classifier(text_body)

        return sent[0]['label']

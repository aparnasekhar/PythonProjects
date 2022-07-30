document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#mail-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Handle sending an email, return to sent inbox after TODO: Not returning to sent inbox
  let form = document.querySelector('#compose-form');
  form.addEventListener('submit', function(ev) {
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
      console.log(result);
    })
    ev.preventDefault();
    load_mailbox('sent');
  });
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      const sections_to_show = [['sender', 5], ['subject', 3], ['timestamp', 4]];
     
      emails.forEach(email => {
        const row_div_element = document.createElement('div');
        row_div_element.classList.add("row","email-line-box", email["read"] ? "read" : "unread");
        sections_to_show.forEach(section => {
          const section_name = section[0];
          const section_size = section[1];
          const div_section = document.createElement('div');
          div_section.classList.add(`col-${section_size}`, `${section_name}-section`);
          div_section.innerHTML = `<p>${email[section_name]}</p>`;
          row_div_element.append(div_section); 
        });
          row_div_element.addEventListener('click', () => load_email(email["id"], mailbox));

      document.querySelector('#emails-view').append(row_div_element);

      })
          console.log(emails);
    });

}

function load_email(email_id, origin_mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'block';

  document.querySelector('#mail-view').innerHTML = '';
  fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
      
        // Print email
            const email_view_div = document.createElement('div');
            email_view_div.classList.add("jumbotron");
            email_view_div.id = 'single_email';
            email_view_div. innerHTML = `<h3>${email["subject"]}</h3>`
            const email_div = document.createElement('div');
            email_div.classList.add("lead");
            email_div.innerHTML = `<strong>From :</strong> ${email["sender"]}<br>
            <strong>To :</strong> ${email["recipients"]}<br> <strong>Subject : </strong>${email["subject"]}<br> <strong>Time :</strong> ${email["timestamp"]}<hr>`
            const email_body = document.createElement('div');
            email_body.classList.add("email-body");
            email_body.innerHTML = `${email["body"]}`;
          
            // Buttons for reply and archive
            const reply_btn = document.createElement('button');
            const archive_btn = document.createElement('button');
            reply_btn.classList.add("btn", "btn-secondary");
            reply_btn.id = "reply";
            archive_btn.classList.add("btn", "btn-secondary");
            archive_btn.id = "archive";
            reply_btn.innerHTML = `Reply`;
            if (email["archived"]) {
              archive_btn.innerHTML = `Unarchive`;}
            else {
              archive_btn.innerHTML = `Archive`;
            }
            
            document.querySelector('#mail-view').append(email_view_div);
            document.querySelector('#single_email').append(email_div, email_body, reply_btn, archive_btn);
            if (origin_mailbox === "sent") {
              document.getElementById("archive").remove();
            }
            reply_btn.addEventListener('click', () => reply_email(email));
            archive_btn.addEventListener('click', () => archive_email(email_id, !email["archived"]));

            fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })   
    });
}

function reply_email(email) {
  compose_email();
  document.querySelector('#compose-recipients').value = email["sender"];
  document.querySelector('#compose-subject').value = "Re: " + email["subject"] ;
  const pre_body_text = `\n \n \n------ On ${email['timestamp']} ${email["sender"]} wrote: \n \n`;
  document.querySelector('#compose-body').value = pre_body_text + email["body"].replace(/^/gm, "\t");
}

function archive_email(email_id, to_archive) {
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: to_archive
    })
  }).then( () => load_mailbox("inbox"));
}
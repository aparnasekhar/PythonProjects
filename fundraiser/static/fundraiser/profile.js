document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#mycampaigns').addEventListener('click', () => load_profile('campaigns'));
    document.querySelector('#mydonations').addEventListener('click', () => load_donations('donations'));
    document.querySelector('#mymessages').addEventListener('click', () => load_chatbox('inbox'));
    document.querySelector('#inbox').addEventListener('click', () => load_chatbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_chatbox('sent'));

    load_profile('campaigns');
    });

    function load_profile(myprofile) {
        document.querySelector('#campaign-view').style.display = 'block';
        document.querySelector('#donation-view').style.display = 'none';
        document.querySelector('#my-messages').style.display = 'none';
       
        document.querySelector('#campaign-view').innerHTML = `<h3>Your Campaigns </h3>`;
        fetch(`/profile/${myprofile}`)
            .then(response => response.json())
            .then(works => {
                works.forEach(work => {
                    const row_div_element = document.createElement('div');
                    row_div_element.classList.add("card");
                    const card_body_div = document.createElement('div');
                    card_body_div.classList.add("card-body");
                    card_body_div.innerHTML = `<h5 class="card-title">${work["title"]}</h5>
                    <p class="card-text"><strong>Amount Needed: </strong> $${work["amount_needed"]}<p>
                    <p class="card-text"><strong>Last Date:</strong>${work["end_date"]}</p>`;
                    row_div_element.append(card_body_div);

                    document.querySelector('#campaign-view').append(row_div_element);
                });
                
            });
    }

    function load_donations(myprofile) {
        document.querySelector('#campaign-view').style.display = 'none';
        document.querySelector('#donation-view').style.display = 'block';
        document.querySelector('#my-messages').style.display = 'none';

        document.querySelector('#donation-view').innerHTML = `<h3>Your Donations </h3>`;
        fetch(`/profile/${myprofile}`)
            .then(response => response.json())
            .then(works => {
                works.forEach(work => {
                    const row_div_element = document.createElement('div');
                    row_div_element.classList.add("card");
                    const card_body_div = document.createElement('div');
                    card_body_div.classList.add("card-body");
                    card_body_div.innerHTML = `<h5 class="card-title">${work["donated_for"]}</h5>
                    <p class="card-text"><strong>Amount Donated: </strong> $${work["donation"]}<p>`;
                    row_div_element.append(card_body_div);

                    document.querySelector('#donation-view').append(row_div_element);
                     
                });
                
            });
    }

    function load_chatbox(chats) {
        document.querySelector('#my-messages').style.display = 'block';
        document.querySelector('#campaign-view').style.display = 'none';
        document.querySelector('#donation-view').style.display = 'none';
        document.querySelector('#message-view').style.display = 'none';
        document.querySelector('#inbox-view').style.display = 'block';

        document.querySelector('#inbox-view').innerHTML = `<h3>Your Messages </h3>`;
        fetch(`/messages/${chats}`)
        .then(response => response.json())
        .then(messages => {
            const ul_element = document.createElement('ul');
            ul_element.classList.add("list-group", "msg-ul");
            messages.forEach(message => {
                
                const li_element = document.createElement('li');
                li_element.classList.add("list-group-item","chat-list", message["read"] ? "read" : "unread");
                li_element.innerHTML = `<strong>${message["sender"]}: </strong>${message["subject"]}<span style="float: right;">${message["timestamp"]}</span>`;
                ul_element.append(li_element);
                li_element.addEventListener('click', () => load_msgdetails(message["id"], chats));
                
                document.querySelector('#inbox-view').append(ul_element);
            });    
         });
    }

    function load_msgdetails(message_id, chats) {
        document.querySelector('#my-messages').style.display = 'block';
        document.querySelector('#campaign-view').style.display = 'none';
        document.querySelector('#donation-view').style.display = 'none';
        document.querySelector('#message-view').style.display = 'block';
        document.querySelector('#inbox-view').style.display = 'none';

        document.querySelector('#message-view').innerHTML = '';
        fetch(`/messages/${chats}/${message_id}`)
        .then(response => response.json())
        .then(message => {
            const message_div = document.createElement('div');
            message_div.classList.add("card", "msg-card");
            const msg_child_div = document.createElement('div');
            msg_child_div.classList.add("card-body");
            msg_child_div.innerHTML = ` <p><strong>From : </strong>${message["sender"]}</p>
            <p><strong>Subject : </strong>${message["subject"]}</p>
            <p><strong>Date : </strong>${message["timestamp"]}</p><hr>
            <div class="msg-body"><p>${message["body"]}</p>
            </div> `;
          
            document.querySelector('#message-view').append(message_div);
            message_div.append(msg_child_div);
            
            fetch(`/messages/${chats}/${message_id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    read: true
                })
            })
        });
        
    }

    
css = """
<style>
.block-container{
    padding:3rem 1rem 10rem !important;
}
.chat-message {
    padding: 0.5rem;
    border-radius: 0.5rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: flex-start;
    transition: transform 0.2s ease, background-color 0.3s ease;
}
.chat-message.user {
    margin-left: auto;
    flex-direction: row-reverse;
}
.chat-message.bot {
    background-color: #475063;
    margin-right: auto;
}
.chat-message:hover {
    transform: scale(1.02);
}
.chat-message .avatar {
    width: 50px;
    height: 50px;
    flex-shrink: 0;
    display: flex;
    justify-content: center;
    align-items: center;
}
.chat-message .avatar img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #fff;
}
.chat-message .message {
    max-width: 85%;
    margin-left: 0.5rem;
    margin-right: 0.5rem;
    padding: 0.75rem 1rem;
    color: #848fa3;
    font-family: 'Arial', sans-serif;
    font-size: 0.9rem;
    line-height: 1.4;
    text-align: left;
    background-color: inherit;
    border-radius: 0.5rem;
    box-shadow: 0 2px 5px darkgray;
}
</style>
"""

user_template = """
<div class="chat-message user">
    <div class="avatar">
        <img src="https://banner2.cleanpng.com/20180920/efk/kisspng-user-logo-information-service-design-1713937950142.webp">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
"""

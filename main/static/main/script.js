
function copyDivToClipboard() {
        // Get the text field
        var copyText = document.getElementById("shortened-url").innerText;
        unsecuredCopyToClipboard(copyText);
        // navigator.clipboard.writeText(copyText);

        // // Alert the copied text
        // alert("Copied the text: " + copyText);
} 

function unsecuredCopyToClipboard(text) {
        const textArea = document.createElement("textarea");
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
                document.execCommand('copy');
        } catch (err) {
                console.error('Unable to copy to clipboard', err);
        }
        document.body.removeChild(textArea);
}

function scrollToSection(id){
        const section = document.getElementById(id);
        section.scrollIntoView({behavior: "smooth"});
}
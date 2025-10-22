emailjs.init({
        publicKey: "novcO9hl9nX-1Ry7A",
      });

document.getElementById("contact_form").addEventListener("submit",function(event){
    event.preventDefault();
    
    const formData = {
        name: document.getElementById("name").value,
        email: document.getElementById("name").value,
        subject: document.getElementById("name").value,
        message: document.getElementById("name").value,
    }

    const serviceID = "service_d04zmce";
    const templateID = "template_8xartji";
    const submitButton = document.getElementById("submit_button");

    submitButton.textContent = "Enviando...";

    emailjs.send(serviceID,templateID,formData)
    .then(() => {
        alert("Menssagem enviada. Entraremos em contato assim que possivel!");
        document.getElementById("contact_form").reset();
    })
    .catch((error) => {
        console.error("Erro ao enviar msg",error);
        alert("erro ao enviar email. por favor entre em contato atraves de contato@kaizo.com.br");
     })
     .finally(()=> { 
        submitButton.textContent = "Enviar nova menssagem"
     });




});
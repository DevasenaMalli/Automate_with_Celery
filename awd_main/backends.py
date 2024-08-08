# your_app/backends.py
from django.core.mail.backends.smtp import EmailBackend
import ssl
import certifi
import smtplib

class SSLEmailBackend(EmailBackend):
    def _create_ssl_context(self):
        ssl_context = ssl.create_default_context()
        ssl_context.load_verify_locations(certifi.where())
        return ssl_context

    def open(self):
        if self.connection:
            return False
        try:
            self.connection =  smtplib.SMTP(self.host, self.port)
            if self.use_tls:
                self.connection.starttls(context=self._create_ssl_context())
            self.connection.login(self.username, self.password)
        except Exception:
            if not self.fail_silently:
                raise 
           
        return True

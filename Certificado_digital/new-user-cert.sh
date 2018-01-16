
# Create the key. This should be done once per cert.
email=$1
if [ $# -ne 1 ]; then

        echo "Usage: \n$0 user@est.fib.upc.edu \n"
        echo "Atenció: feu servir el EMAIL UPC"
	echo
        exit 1
fi

# Fill the necessary certificate data
CONFIG="user-cert.conf"
cat >$CONFIG <<EOT
[ req ]
distinguished_name		= req_distinguished_name
string_mask			= nombstr
req_extensions			= v3_req
[ req_distinguished_name ]
commonName			= Common Name (eg, John Doe)
commonName_max			= 64
commonName_default              = $email
emailAddress			= UPC Email Address
emailAddress_max		= 40
emailAddress_default            = $email
[ v3_req ]
nsCertType			= client,email
basicConstraints		= critical,CA:false
EOT

echo "Fill in certificate data, creaete a new EC_p521 private key and request for a certificate"
openssl req -newkey ec:curva_a_usar_p521 -config  $CONFIG  -out $email.req -keyout $email.private_key
echo "."
rm -f $CONFIG


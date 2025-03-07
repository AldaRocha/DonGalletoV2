using Jose;
using Newtonsoft.Json;
using System;
using System.IO;
using System.Security.Cryptography.X509Certificates;
using System.Text;

namespace Security
{
    public class Firewall
    {
        private readonly byte[] Secret;
        private readonly string PWD;
        private readonly JwsAlgorithm Algorithm;
        public bool JWE;
        private readonly string CERT;
        X509Certificate2 Certificate = null;
        public byte[] Bytes;

        public Firewall()
        {
            this.PWD = "DonGalleto2024";
            this.Secret = Encoding.ASCII.GetBytes(this.PWD);
            this.Algorithm = JwsAlgorithm.HS256;
            this.JWE = false;
            this.CERT = "RCA.p12";
            this.Bytes = File.ReadAllBytes(this.CERT);
        }

        public string Encode(dynamic payload)
        {
            return JWT.Encode(payload, this.Secret, this.Algorithm);
        }

        public string EncodeJWE2(dynamic payload)
        {
            var publicKey = this.Certificate.PublicKey.Key;
            return JWT.Encode(payload, publicKey, JweAlgorithm.RSA_OAEP, JweEncryption.A256CBC_HS512);
        }

        public T Decode2<T>(string token)
        {
            if (this.JWE)
            {
                var privateKey = this.Certificate.PrivateKey;
                return JsonConvert.DeserializeObject<T>(JWT.Decode(token, privateKey, JweAlgorithm.RSA_OAEP, JweEncryption.A256CBC_HS512));
            }
            else
            {
                return JsonConvert.DeserializeObject<T>(JWT.Decode(token, this.Secret, this.Algorithm));
            }
        }

        public string EncodeJWE(dynamic payload)
        {
            var publicKey = new X509Certificate2(this.Bytes, this.PWD, X509KeyStorageFlags.Exportable | X509KeyStorageFlags.MachineKeySet | X509KeyStorageFlags.PersistKeySet).PublicKey.Key;
            return JWT.Encode(payload, publicKey, JweAlgorithm.RSA_OAEP, JweEncryption.A256CBC_HS512);
        }

        public T Decode<T>(string token)
        {
            if (this.JWE)
            {
                try
                {
                    var privateKey = new X509Certificate2(this.Bytes, this.PWD, X509KeyStorageFlags.MachineKeySet).GetRSAPrivateKey();
                    return JsonConvert.DeserializeObject<T>(JWT.Decode(token, privateKey, JweAlgorithm.RSA_OAEP, JweEncryption.A256CBC_HS512));
                }
                catch (Exception e)
                {
                    return this.Decode<T>(token);
                }
            }
            else
            {
                return JsonConvert.DeserializeObject<T>(JWT.Decode(token, this.Secret, this.Algorithm));
            }
        }
    }
}

using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Security.Cryptography.X509Certificates;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Server.Kestrel.Core;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

namespace Servicios.Fachada
{
    public class Program
    {
        public static void Main(string[] args)
        {
            CreateHostBuilder(args).Build().Run();
        }

        public static IHostBuilder CreateHostBuilder(string[] args) =>
            Host.CreateDefaultBuilder(args)
                .ConfigureWebHostDefaults(webBuilder =>
                {
                    webBuilder.UseUrls("http://0.0.0.0:5030");

                    webBuilder.UseStartup<Startup>();   
                    webBuilder.UseKestrel(o => { o.Limits.KeepAliveTimeout = TimeSpan.FromMinutes(10); });
                });
    }

    public static class KestrelServerOptionsExtensions
        {
            public static void ConfigureEndpoints(this KestrelServerOptions options)
            {
                var configuration = options.ApplicationServices.GetRequiredService<IConfiguration>();
                var environment = options.ApplicationServices.GetRequiredService<Microsoft.AspNetCore.Hosting.IHostingEnvironment>();

                var endpoints = configuration.GetSection("HttpServer:Endpoints")
                    .GetChildren()
                    .ToDictionary(section => section.Key, section =>
                    {
                        var endpoint = new EndpointConfiguration();
                        section.Bind(endpoint);
                        return endpoint;
                    });

                foreach (var endpoint in endpoints)
                {
                    var config = endpoint.Value;
                    var port = config.Port ?? (config.Scheme == "https" ? 443 : 80);

                    var ipAddresses = new List<IPAddress>();
                    if (config.Host == "localhost")
                    {
                        ipAddresses.Add(IPAddress.IPv6Loopback);
                        ipAddresses.Add(IPAddress.Loopback);
                    }
                    else if (IPAddress.TryParse(config.Host, out var address))
                    {
                        ipAddresses.Add(address);
                    }
                    else
                    {
                        ipAddresses.Add(IPAddress.IPv6Any);
                    }

                    foreach (var address in ipAddresses)
                    {
                        options.Listen(address, port,
                            listenOptions =>
                            {
                                if (config.Scheme == "https")
                                {
                                    var certificate = LoadCertificate(config, environment);
                                    listenOptions.UseHttps(certificate);
                                    listenOptions.Protocols = Microsoft.AspNetCore.Server.Kestrel.Core.HttpProtocols.Http1;
                                }
                            });
                    }
                }
            }

            private static X509Certificate2 LoadCertificate(EndpointConfiguration config, Microsoft.AspNetCore.Hosting.IHostingEnvironment environment)
            {
                if (config.StoreName != null && config.StoreLocation != null)
                {
                    using (var store = new X509Store(config.StoreName, Enum.Parse<StoreLocation>(config.StoreLocation)))
                    {
                        store.Open(OpenFlags.ReadOnly);
                        var certificate = store.Certificates.Find(
                            X509FindType.FindBySubjectName,
                            config.Host,
                            validOnly: !environment.IsDevelopment());

                        if (certificate.Count == 0)
                        {
                            throw new InvalidOperationException($"Certificate not found for {config.Host}.");
                        }

                        return certificate[0];
                    }
                }

                if (config.FilePath != null && config.Password != null)
                {
                    return new X509Certificate2(config.FilePath, config.Password);
                }

                throw new InvalidOperationException("No valid certificate configuration found for the current endpoint.");
            }
        }

        public class EndpointConfiguration
        {
            public string Host { get; set; }
            public int? Port { get; set; }
            public string Scheme { get; set; }
            public string StoreName { get; set; }
            public string StoreLocation { get; set; }
            public string FilePath { get; set; }
            public string Password { get; set; }
        }
    
}

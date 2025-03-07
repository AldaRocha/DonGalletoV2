using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Servicios.Datos;

namespace Servicios.Fachada
{
    public class Startup
    {
#pragma warning disable CS0414 // El campo 'Startup.Conexion' está asignado pero su valor nunca se usa
        int Conexion = 4;
#pragma warning restore CS0414 // El campo 'Startup.Conexion' está asignado pero su valor nunca se usa

        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;

        }

        public IConfiguration Configuration;

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddCors();
            services.AddControllers();
            services.AddResponseCompression(options =>
            {
                options.EnableForHttps = true;
            });

            string connectionString = Configuration.GetConnectionString("DefaultConnection");
            services.AddDbContextPool<AccesoDatos>(options => options.UseSqlServer(connectionString));
            services.AddDbContext<AccesoDatos>(options => { 
               
                options.UseSqlServer(connectionString); });
           
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }

            app.UseCors(builder => builder
                .WithOrigins("*")
                .AllowAnyHeader()
                .AllowAnyMethod()
            );

            app.UseRouting();

            app.UseAuthorization();
            app.UseResponseCompression();

            app.UseEndpoints(endpoints =>
            {
                endpoints.MapControllers();
            });
        }
    }
}

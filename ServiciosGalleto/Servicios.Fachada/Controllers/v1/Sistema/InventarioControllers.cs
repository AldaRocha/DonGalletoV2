using Microsoft.AspNetCore.Mvc;
using Security;
using Servicios.Datos;
using Servicios.Entidad.ViewModel;
using Servicios.Fachada.AppService;
using Servicios.Fachada.CQRS;
using System;
using System.Collections.Generic;

namespace Servicios.Fachada.Controllers.v1.Sistema
{
    [Route("api/v1/almacen")]
    public class InventarioControllers : ControllerBase
    {
        AccesoDatos DbContext;
        Response response;

        public InventarioControllers(AccesoDatos DbContext)
        {
            this.DbContext = DbContext;
            this.response = new Response();
        }

        [HttpGet("{Activo}")]
        public ActionResult<Response> GetAlmacen(int activo)
        {
            try
            {
                InventarioAppService ias = new InventarioAppService();

                List<InventarioViewModel> data = ias.GetInventario(DbContext, activo);

                return response.Ok("", data);
            }
            catch (Exception ex)
            {
                return new ObjectResult(new { message = ex.Message });
            }
        }

        [HttpPost]
        public ActionResult<Response> AgregarAlmacen([FromBody] RequestInterface request)
        {
            try
            {
                List<InventarioViewModel> dataList = request.getData<List<InventarioViewModel>>();
                InventarioAppService ias = new InventarioAppService();

                string mensaje = ias.AgregarInventario(DbContext, dataList);

                return response.Ok(mensaje);
            }
            catch (Exception ex)
            {
                return new ObjectResult(new { message = ex.Message });
            }
        }

        [HttpPut("{id}")]
        public ActionResult<Response> ActualizarAlmacen(int id, [FromBody] RequestInterface request)
        {
            try
            {
                InventarioViewModel data = request.getData<InventarioViewModel>();
                InventarioAppService ias = new InventarioAppService();

                string mensaje = ias.ActualizarInventario(DbContext, id, data);

                return response.Ok(mensaje);
            }
            catch (Exception ex)
            {
                return new ObjectResult(new { message = ex.Message });
            }
        }

        [HttpDelete("{id}")]
        public ActionResult<Response> DesactivarAlmacen(int id)
        {
            try
            {
                InventarioCQRS icqrs = new InventarioCQRS();

                string mensaje = icqrs.DesactivarInventario(DbContext, id);

                return response.Ok(mensaje);
            }
            catch (Exception ex)
            {
                return new ObjectResult(new { message = ex.Message });
            }
        }
    }
}

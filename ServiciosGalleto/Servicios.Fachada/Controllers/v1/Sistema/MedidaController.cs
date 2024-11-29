using Microsoft.AspNetCore.Mvc;
using Security;
using Servicios.Datos;
using Servicios.Entidad.ViewModel;
using Servicios.Fachada.AppService;
using System.Collections.Generic;
using System;

namespace Servicios.Fachada.Controllers.v1.Sistema
{
    [Route("api/v1/medida")]
    public class MedidaController : ControllerBase
    {
        AccesoDatos DbContext;
        Response response;

        public MedidaController(AccesoDatos DbContext)
        {
            this.DbContext = DbContext;
            this.response = new Response();
        }

        [HttpGet]
        public ActionResult<Response> GetMedida()
        {
            try
            {
                MedidaAppService mas = new MedidaAppService();

                List<MedidaViewModel> data = mas.GetMedida(DbContext);

                return response.Ok("", data);
            }
            catch (Exception ex)
            {
                return new ObjectResult(new { message = ex.Message });
            }
        }
    }
}

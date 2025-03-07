using Microsoft.AspNetCore.Mvc;
using Security;
using Servicios.Datos;
using Servicios.Entidad.ViewModel;
using Servicios.Fachada.AppService;
using System.Collections.Generic;
using System;
using Servicios.Fachada.DAO;
using Servicios.Entidad.Model;

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
                MedidaDAO mdao = new MedidaDAO();

                List<Medida> lista = mdao.GetAllMedida(DbContext);
                List<MedidaViewModel> dataList = new List<MedidaViewModel>();

                foreach (Medida i in lista)
                {
                    MedidaViewModel model = new MedidaViewModel();

                    model.id = i.MedidaId;
                    model.nombre = i.Nombre;

                    dataList.Add(model);
                }

                return response.Ok("", dataList);
            }
            catch (Exception ex)
            {
                return new ObjectResult(new { message = ex.Message });
            }
        }
    }
}

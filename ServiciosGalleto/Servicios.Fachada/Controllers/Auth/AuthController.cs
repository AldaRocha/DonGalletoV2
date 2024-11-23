using System;
using Microsoft.AspNetCore.Mvc;
using Servicios.Datos;
using Security;
using Security.Partial;
using Security.Auth;

namespace Servicios.Fachada.Controllers
{
    [Route("api/auth")]
    public class AuthController : ControllerBase
    {
        #region Variables

        AccesoDatos DbContext;
        Response response;

        #endregion

        #region Contructor

        public AuthController(AccesoDatos DbContext)
        {
            this.DbContext = DbContext;
            this.response = new Response();
        }

        #endregion

        #region Metodos

        [HttpPost("login")]
        public ActionResult<Response> Login([FromBody] RequestInterface request)
        {
            try
            {
                bool JWE = this.response.IsJWE();
                ResponseInterface responseInterface = new Auth(this.DbContext, request).Connect(this.response, JWE);
                if (responseInterface.error)
                {
                    this.HttpContext.Response.StatusCode = responseInterface.status;
                    return this.response.Error(responseInterface.message);
                }

                return this.response.Ok("", responseInterface.authData);
            }
            catch (Exception ex)
            {
                this.HttpContext.Response.StatusCode = response.BadRequest;
                return response.Error(ex.Message);
            }
        }

        #endregion
    }
}

using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Text;

namespace Servicios.Entidad.Model
{
    public class Medida
    {
        [Key]
        public int MedidaId { get; set; }
        public string Nombre { get; set; }
    }
}

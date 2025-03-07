using Servicios.Entidad.Model;
using System;
using System.Collections.Generic;
using System.Text;

namespace Servicios.Entidad.ViewModel
{
    public class InventarioViewModel
    {
        public int? id { get; set; }
        public string? nombre { get; set; }
        public string? fechaCompra { get; set; }
        public string? fechaVencimiento { get; set; }
        public int? activo { get; set; }
        public decimal? cantidad { get; set; }
        public decimal? precio { get; set; }
        public int? porcentaje { get; set; }
        public string? proveedor { get; set; }
        public int idMedida { get; set; }
        public MedidaViewModel? medida { get; set; }
    }
}

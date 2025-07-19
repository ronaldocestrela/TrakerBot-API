using Microsoft.AspNetCore.Http;
using TrakerBot.Infrastructure.DTOs;

namespace TrakerBot.Infrastructure.Interfaces;

public interface IPhotoService
{
    Task<PhotoUploadResult?> UpLoadPhoto(IFormFile file);
    Task<string> DeletePhoto(string publicId);
}

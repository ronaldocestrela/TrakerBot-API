using System.Security.Claims;
using Microsoft.AspNetCore.Http;
using TrakerBot.Core.Entities;
using TrakerBot.Infrastructure.Interfaces;
using TrakerBot.Infrastructure.UserInfo;
using TrakerBot.Persistance;

namespace TrakerBot.Infrastructure.Security;

public class UserAccessor(IHttpContextAccessor httpContextAccessor, ApplicationDbContext applicationDbContext) : IUserAccessor
{
    public async Task<UserInfoDto> GetUserAsync()
    {
        var user = await applicationDbContext.Users.FindAsync(GetUserId())
            ?? throw new UnauthorizedAccessException("No user is logged in");
        return new UserInfoDto
        {
            Id = user.Id,
            FirstName = user.FirstName!,
            LastName = user.LastName!,
            Email = user.Email!,
            ProfilePictureUrl = user.ProfilePictureUrl!,
        };
    }

    public string GetUserId()
    {
        return httpContextAccessor.HttpContext?.User.FindFirstValue(ClaimTypes.NameIdentifier)
            ?? throw new Exception("User not found");
    }

    public string GetUserRoleNameByUserIdAsync(string userId)
    {
        var role = applicationDbContext.UserRoles.FirstOrDefault(ur => ur.UserId == userId) ?? throw new Exception("User not found");

        var roleName = applicationDbContext.Roles.FirstOrDefault(r => r.Id == role.RoleId)?.Name ?? "User";

        return roleName;
    }

    public Task<ApplicationUser> GetUserWithPhotosAsync()
    {
        throw new NotImplementedException();
    }
}

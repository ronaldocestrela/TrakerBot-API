using FluentValidation;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc.Authorization;
using Microsoft.EntityFrameworkCore;
using TrakerBot.API.Middleware;
using TrakerBot.Application.Core;
using TrakerBot.Application.FakeEmail;
using TrakerBot.Core.Entities;
using TrakerBot.Infrastructure;
using TrakerBot.Infrastructure.Interfaces;
using TrakerBot.Infrastructure.Photos;
using TrakerBot.Infrastructure.Security;
using TrakerBot.Persistance;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddDbContext<ApplicationDbContext>(options =>
{
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnectionSqlServer"));
});

builder.Services.AddAutoMapper(cfg => { }, typeof(MappingProfiles).Assembly);
// builder.Services.AddValidatorsFromAssemblyContaining<CreateExpertValidator>();
builder.Services.AddTransient<ExceptionMiddleware>();
builder.Services.Configure<CloudinarySettings>(builder.Configuration.GetSection("CloudinarySettings"));

builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(builder =>
    {
        builder.WithOrigins("http://localhost:3000", "https://localhost:3000")
            .AllowCredentials()
            .AllowAnyMethod()
            .AllowAnyHeader();
    });
});

builder.Services.AddIdentityApiEndpoints<ApplicationUser>(opt =>
{
    opt.User.RequireUniqueEmail = true;
}).AddRoles<ApplicationRole>().AddEntityFrameworkStores<ApplicationDbContext>();

// builder.Services.AddMediatR(x => {
//     x.RegisterServicesFromAssemblyContaining<CreateExpertValidator>();
//     x.AddOpenBehavior(typeof(ValidationBehavior<,>));
// });

builder.Services.AddControllers(opt =>
{
    var policy = new AuthorizationPolicyBuilder().RequireAuthenticatedUser().Build();
    opt.Filters.Add(new AuthorizeFilter(policy));
});
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();

builder.Services.AddScoped<IUserAccessor, UserAccessor>();
builder.Services.AddScoped<IPhotoService, PhotoService>();

builder.Services.AddTransient<IEmailSender<ApplicationUser>, DummyEmailSender>();

builder.Services.Configure<IdentityOptions>(options =>
{
    // Configurações de senha e lockout se desejar
});

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseHttpsRedirection();

app.UseAuthentication();
app.UseAuthorization();

app.MapGroup("api").MapIdentityApi<ApplicationUser>();

app.MapControllers();

app.Run();
